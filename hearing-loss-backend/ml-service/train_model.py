import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import warnings
warnings.filterwarnings('ignore')

print("Starting XGBoost model training process...")

# --- 1. Load and Validate Dataset ---
try:
    df = pd.read_csv('synthetic_hearing_loss_data.csv')
    print(f"Dataset loaded successfully. Shape: {df.shape}")

    # Basic data validation
    print(f"Missing values per column:")
    missing_vals = df.isnull().sum()
    if missing_vals.sum() > 0:
        print(missing_vals[missing_vals > 0])
    else:
        print("No missing values found.")

except FileNotFoundError:
    print("Error: synthetic_hearing_loss_data.csv not found.")
    print("Please run the data generation script first.")
    exit()
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

# --- 2. Enhanced Feature Engineering ---
print("Creating engineered features...")

# Air-Bone Gap (ABG) features - crucial for hearing loss classification
for freq in [500, 1000, 2000, 4000]:
    df[f'abg_l_{freq}'] = df[f'ac_l_{freq}'] - df[f'bc_l_{freq}']
    df[f'abg_r_{freq}'] = df[f'ac_r_{freq}'] - df[f'bc_r_{freq}']

# Pure Tone Averages (PTA) - standard clinical measures
df['pta_l'] = (df['ac_l_500'] + df['ac_l_1000'] + df['ac_l_2000'] + df['ac_l_4000']) / 4
df['pta_r'] = (df['ac_r_500'] + df['ac_r_1000'] + df['ac_r_2000'] + df['ac_r_4000']) / 4
df['pta_better'] = np.minimum(df['pta_l'], df['pta_r'])
df['pta_worse'] = np.maximum(df['pta_l'], df['pta_r'])
df['pta_asymmetry'] = np.abs(df['pta_l'] - df['pta_r'])

# High-frequency average (important for noise-induced hearing loss)
df['hf_avg_l'] = (df['ac_l_4000'] + df['ac_l_8000']) / 2
df['hf_avg_r'] = (df['ac_r_4000'] + df['ac_r_8000']) / 2

# Speech-audiometry derived features
df['srt_pta_diff_l'] = df['srt_l'] - df['pta_l']  # Important for ANSD detection
df['srt_pta_diff_r'] = df['srt_r'] - df['pta_r']

# ABG averages (important for conductive loss detection)
df['abg_avg_l'] = (df['abg_l_500'] + df['abg_l_1000'] + df['abg_l_2000'] + df['abg_l_4000']) / 4
df['abg_avg_r'] = (df['abg_r_500'] + df['abg_r_1000'] + df['abg_r_2000'] + df['abg_r_4000']) / 4

# Bilateral features
df['bilateral_loss'] = ((df['pta_l'] > 25) & (df['pta_r'] > 25)).astype(int)
df['unilateral_loss'] = (((df['pta_l'] > 25) & (df['pta_r'] <= 25)) |
                         ((df['pta_r'] > 25) & (df['pta_l'] <= 25))).astype(int)

print(f"Feature engineering complete. New shape: {df.shape}")

# --- 3. Data Quality Checks ---
print("Performing data quality checks...")

# Check for unrealistic values
audiometric_cols = [col for col in df.columns if col.startswith(('ac_', 'bc_', 'srt_'))]
for col in audiometric_cols:
    if df[col].min() < -10 or df[col].max() > 120:
        print(f"Warning: {col} has values outside normal range (-10 to 120 dB)")

# Check ABG values (should be realistic)
abg_cols = [col for col in df.columns if col.startswith('abg_')]
for col in abg_cols:
    if df[col].min() < -20 or df[col].max() > 70:
        print(f"Warning: {col} has unrealistic air-bone gap values")

print("Data quality checks complete.")

# --- 4. Target Variable Analysis ---
print("\nTarget variable distribution:")
for target in ['hearing_loss', 'hearing_loss_type', 'hearing_loss_severity']:
    print(f"\n{target}:")
    print(df[target].value_counts().sort_index())

# --- 5. Preprocess Target Variables ---
target_categorical_cols = ['hearing_loss_type', 'hearing_loss_severity']
label_encoders = {}

for col in target_categorical_cols:
    le = LabelEncoder()
    df[col + '_encoded'] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le

    # Print encoding mapping
    print(f"\n{col} encoding mapping:")
    for i, label in enumerate(le.classes_):
        print(f"  {i}: {label}")

# Save label encoders
joblib.dump(label_encoders, 'label_encoders.pkl')
print("\nLabel encoders saved.")

# --- 6. Define Features and Targets ---
# Use encoded versions of categorical targets
target_cols = ['hearing_loss', 'hearing_loss_type_encoded', 'hearing_loss_severity_encoded']
exclude_cols = target_cols + ['hearing_loss_type', 'hearing_loss_severity']  # Exclude original categorical columns

X = df.drop(columns=exclude_cols)
y = df[target_cols]

# Handle categorical input features with one-hot encoding
categorical_input_cols = ['tymp_type_l', 'tymp_type_r']
X = pd.get_dummies(X, columns=categorical_input_cols, drop_first=False)

print(f"\nFeature matrix shape: {X.shape}")
print(f"Target matrix shape: {y.shape}")

# --- 7. Save Model Configuration ---
model_columns = X.columns.tolist()
feature_info = {
    'model_columns': model_columns,
    'n_features': len(model_columns),
    'categorical_columns': [col for col in X.columns if any(cat in col for cat in ['tymp_type'])],
    'engineered_features': [col for col in X.columns if any(feat in col for feat in ['abg_', 'pta_', 'hf_avg_', 'srt_pta_diff_'])]
}

joblib.dump(feature_info, 'model_feature_info.pkl')
joblib.dump(model_columns, 'model_columns.pkl')  # Backward compatibility
print(f"Model feature info saved. Total features: {len(model_columns)}")

# --- 8. Train-Test Split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y['hearing_loss']
)

print(f"Training set shape: {X_train.shape}")
print(f"Test set shape: {X_test.shape}")

# --- 9. Model Configuration and Training ---
print("\nConfiguring XGBoost model...")

# Optimized parameters for hearing loss classification
xgb_params = {
    'n_estimators': 300,
    'max_depth': 6,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'min_child_weight': 1,
    'gamma': 0,
    'reg_alpha': 0.1,
    'reg_lambda': 1,
    'random_state': 42,
    'n_jobs': -1,
    'use_label_encoder': False,
    'eval_metric': 'mlogloss'
}

base_classifier = xgb.XGBClassifier(**xgb_params)
model = MultiOutputClassifier(base_classifier, n_jobs=-1)

print("Training the XGBoost model...")
model.fit(X_train, y_train)
print("Model training complete.")

# --- 10. Model Evaluation ---
print("\nEvaluating model performance...")

y_pred = model.predict(X_test)
y_pred_df = pd.DataFrame(y_pred, columns=target_cols)

# Calculate accuracy for each target
for i, target in enumerate(target_cols):
    accuracy = accuracy_score(y_test.iloc[:, i], y_pred_df.iloc[:, i])
    print(f"{target} accuracy: {accuracy:.4f}")

# Detailed classification report for hearing loss detection
print("\nDetailed evaluation for hearing_loss (binary classification):")
print(classification_report(y_test['hearing_loss'], y_pred_df['hearing_loss']))

# Confusion matrix for hearing loss type
if len(label_encoders['hearing_loss_type'].classes_) > 1:
    print("\nConfusion Matrix for hearing_loss_type:")
    cm = confusion_matrix(y_test['hearing_loss_type_encoded'], y_pred_df['hearing_loss_type_encoded'])
    print(cm)

# --- 11. Feature Importance Analysis ---
print("\nAnalyzing feature importance...")

# Get feature importance for the first estimator (hearing_loss prediction)
feature_importance = model.estimators_[0].feature_importances_
importance_df = pd.DataFrame({
    'feature': model_columns,
    'importance': feature_importance
}).sort_values('importance', ascending=False)

print("\nTop 15 most important features:")
print(importance_df.head(15))

# Save feature importance
importance_df.to_csv('feature_importance.csv', index=False)
print("Feature importance saved to 'feature_importance.csv'")

# --- 12. Save the Final Model ---
model_artifacts = {
    'model': model,
    'feature_info': feature_info,
    'label_encoders': label_encoders,
    'training_accuracy': {
        target: accuracy_score(y_test.iloc[:, i], y_pred_df.iloc[:, i])
        for i, target in enumerate(target_cols)
    }
}

model_filename = 'hearing_loss_model.pkl'
joblib.dump(model_artifacts, model_filename)
joblib.dump(model, 'hearing_loss_model_only.pkl')  # Just the model for backward compatibility

print(f"\nModel and artifacts saved successfully:")
print(f"- Main model file: '{model_filename}'")
print(f"- Model only: 'hearing_loss_model_only.pkl'")
print(f"- Label encoders: 'label_encoders.pkl'")
print(f"- Feature info: 'model_feature_info.pkl'")
print(f"- Feature importance: 'feature_importance.csv'")

# --- 13. Model Summary ---
print(f"\n{'='*50}")
print("MODEL TRAINING SUMMARY")
print(f"{'='*50}")
print(f"Dataset size: {df.shape[0]} patients")
print(f"Features used: {len(model_columns)}")
print(f"Training samples: {X_train.shape[0]}")
print(f"Test samples: {X_test.shape[0]}")

print(f"\nModel Performance:")
for i, target in enumerate(target_cols):
    accuracy = accuracy_score(y_test.iloc[:, i], y_pred_df.iloc[:, i])
    print(f"- {target}: {accuracy:.1%} accuracy")

print(f"\nHearing Loss Distribution in Dataset:")
hl_dist = df['hearing_loss'].value_counts()
print(f"- Normal hearing: {hl_dist[0]} ({hl_dist[0]/len(df)*100:.1f}%)")
print(f"- Hearing loss: {hl_dist[1]} ({hl_dist[1]/len(df)*100:.1f}%)")

print(f"\n✅ Model training completed successfully!")
print("The model is ready for deployment and prediction.")