from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict
import pandas as pd
import numpy as np
import joblib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Pydantic Model for Data Validation ---
class PredictionRequest(BaseModel):
    # Patient demographics and history
    age: int = Field(..., ge=0, le=120, description="Patient age in years")
    sex: int = Field(..., ge=0, le=1, description="Sex (0=Female, 1=Male)")
    genetic_history: int = Field(..., ge=0, le=1, description="Genetic history of hearing loss")
    noise_exposure_history: int = Field(..., ge=0, le=1, description="History of noise exposure")
    tinnitus: int = Field(..., ge=0, le=1, description="Presence of tinnitus")
    vertigo_dizziness: int = Field(..., ge=0, le=1, description="Presence of vertigo/dizziness")
    hearing_difficulty_in_noise: int = Field(..., ge=0, le=1, description="Difficulty hearing in noise")

    # Left ear audiometry (Air Conduction)
    ac_l_250: float = Field(..., ge=-10, le=120, description="Left AC at 250Hz (dB HL)")
    ac_l_500: float = Field(..., ge=-10, le=120, description="Left AC at 500Hz (dB HL)")
    ac_l_1000: float = Field(..., ge=-10, le=120, description="Left AC at 1000Hz (dB HL)")
    ac_l_2000: float = Field(..., ge=-10, le=120, description="Left AC at 2000Hz (dB HL)")
    ac_l_4000: float = Field(..., ge=-10, le=120, description="Left AC at 4000Hz (dB HL)")
    ac_l_8000: float = Field(..., ge=-10, le=120, description="Left AC at 8000Hz (dB HL)")

    # Left ear audiometry (Bone Conduction)
    bc_l_500: float = Field(..., ge=-10, le=120, description="Left BC at 500Hz (dB HL)")
    bc_l_1000: float = Field(..., ge=-10, le=120, description="Left BC at 1000Hz (dB HL)")
    bc_l_2000: float = Field(..., ge=-10, le=120, description="Left BC at 2000Hz (dB HL)")
    bc_l_4000: float = Field(..., ge=-10, le=120, description="Left BC at 4000Hz (dB HL)")

    # Left ear speech audiometry and immittance
    srt_l: float = Field(..., ge=-10, le=120, description="Left Speech Reception Threshold (dB HL)")
    wrs_l: float = Field(..., ge=0, le=100, description="Left Word Recognition Score (%)")
    tymp_type_l: str = Field(..., pattern="^(A|As|Ad|B|C)$", description="Left Tympanogram Type")

    # Right ear audiometry (Air Conduction)
    ac_r_250: float = Field(..., ge=-10, le=120, description="Right AC at 250Hz (dB HL)")
    ac_r_500: float = Field(..., ge=-10, le=120, description="Right AC at 500Hz (dB HL)")
    ac_r_1000: float = Field(..., ge=-10, le=120, description="Right AC at 1000Hz (dB HL)")
    ac_r_2000: float = Field(..., ge=-10, le=120, description="Right AC at 2000Hz (dB HL)")
    ac_r_4000: float = Field(..., ge=-10, le=120, description="Right AC at 4000Hz (dB HL)")
    ac_r_8000: float = Field(..., ge=-10, le=120, description="Right AC at 8000Hz (dB HL)")

    # Right ear audiometry (Bone Conduction)
    bc_r_500: float = Field(..., ge=-10, le=120, description="Right BC at 500Hz (dB HL)")
    bc_r_1000: float = Field(..., ge=-10, le=120, description="Right BC at 1000Hz (dB HL)")
    bc_r_2000: float = Field(..., ge=-10, le=120, description="Right BC at 2000Hz (dB HL)")
    bc_r_4000: float = Field(..., ge=-10, le=120, description="Right BC at 4000Hz (dB HL)")

    # Right ear speech audiometry and immittance
    srt_r: float = Field(..., ge=-10, le=120, description="Right Speech Reception Threshold (dB HL)")
    wrs_r: float = Field(..., ge=0, le=100, description="Right Word Recognition Score (%)")
    tymp_type_r: str = Field(..., pattern="^(A|As|Ad|B|C)$", description="Right Tympanogram Type")

    # Advanced diagnostic tests (Optional)
    oae_500_present: Optional[int] = Field(0, ge=0, le=1, description="OAE present at 500Hz")
    oae_1000_present: Optional[int] = Field(0, ge=0, le=1, description="OAE present at 1000Hz")
    oae_4000_present: Optional[int] = Field(0, ge=0, le=1, description="OAE present at 4000Hz")
    abr_wave_i_latency: Optional[float] = Field(0.0, ge=0, le=10, description="ABR Wave I latency (ms)")
    abr_wave_iii_latency: Optional[float] = Field(0.0, ge=0, le=10, description="ABR Wave III latency (ms)")
    abr_wave_v_latency: Optional[float] = Field(0.0, ge=0, le=10, description="ABR Wave V latency (ms)")
    abr_wave_v_absent: Optional[int] = Field(0, ge=0, le=1, description="ABR Wave V absent")

class PredictionResponse(BaseModel):
    hearing_loss: str
    hearing_loss_type: str
    hearing_loss_severity: str
    confidence_scores: dict
    clinical_summary: dict

# --- Load Model Artifacts ---
def load_model_artifacts():
    """Load all required model artifacts with error handling"""
    try:
        # Try to load the comprehensive model artifacts first
        model_artifacts = joblib.load('hearing_loss_model.pkl')
        if isinstance(model_artifacts, dict) and 'model' in model_artifacts:
            model = model_artifacts['model']
            label_encoders = model_artifacts.get('label_encoders', {})
            feature_info = model_artifacts.get('feature_info', {})
            model_columns = feature_info.get('model_columns', [])
        else:
            # Fallback to individual files
            model = model_artifacts
            label_encoders = joblib.load('label_encoders.pkl')
            try:
                feature_info = joblib.load('model_feature_info.pkl')
                model_columns = feature_info['model_columns']
            except FileNotFoundError:
                model_columns = joblib.load('model_columns.pkl')
                feature_info = {'model_columns': model_columns}
        logger.info(f"Model artifacts loaded successfully. Features: {len(model_columns)}")
        return model, label_encoders, feature_info, model_columns

    except FileNotFoundError as e:
        logger.error(f"Model files not found: {e}")
        logger.error("Please run the training script first.")
        return None, None, None, None
    except Exception as e:
        logger.error(f"Error loading model artifacts: {e}")
        return None, None, None, None

# Load model artifacts on startup
model, label_encoders, feature_info, model_columns = load_model_artifacts()

# Initialize FastAPI app
app = FastAPI(
    title="Hearing Loss Prediction API",
    description="Advanced hearing loss classification using XGBoost with comprehensive audiological features",
    version="2.0.0"
)

def perform_feature_engineering(data_df: pd.DataFrame) -> pd.DataFrame:
    """Perform EXACT feature engineering as in training script"""

    # Air-Bone Gap (ABG) features
    for freq in [500, 1000, 2000, 4000]:
        data_df[f'abg_l_{freq}'] = data_df[f'ac_l_{freq}'] - data_df[f'bc_l_{freq}']
        data_df[f'abg_r_{freq}'] = data_df[f'ac_r_{freq}'] - data_df[f'bc_r_{freq}']

    # Pure Tone Averages (PTA)
    data_df['pta_l'] = (data_df['ac_l_500'] + data_df['ac_l_1000'] +
                        data_df['ac_l_2000'] + data_df['ac_l_4000']) / 4
    data_df['pta_r'] = (data_df['ac_r_500'] + data_df['ac_r_1000'] +
                        data_df['ac_r_2000'] + data_df['ac_r_4000']) / 4
    data_df['pta_better'] = np.minimum(data_df['pta_l'], data_df['pta_r'])
    data_df['pta_worse'] = np.maximum(data_df['pta_l'], data_df['pta_r'])
    data_df['pta_asymmetry'] = np.abs(data_df['pta_l'] - data_df['pta_r'])

    # High-frequency averages
    data_df['hf_avg_l'] = (data_df['ac_l_4000'] + data_df['ac_l_8000']) / 2
    data_df['hf_avg_r'] = (data_df['ac_r_4000'] + data_df['ac_r_8000']) / 2

    # Speech-audiometry derived features
    data_df['srt_pta_diff_l'] = data_df['srt_l'] - data_df['pta_l']
    data_df['srt_pta_diff_r'] = data_df['srt_r'] - data_df['pta_r']

    # ABG averages
    data_df['abg_avg_l'] = (data_df['abg_l_500'] + data_df['abg_l_1000'] +
                            data_df['abg_l_2000'] + data_df['abg_l_4000']) / 4
    data_df['abg_avg_r'] = (data_df['abg_r_500'] + data_df['abg_r_1000'] +
                            data_df['abg_r_2000'] + data_df['abg_r_4000']) / 4

    # Bilateral features
    data_df['bilateral_loss'] = ((data_df['pta_l'] > 25) & (data_df['pta_r'] > 25)).astype(int)
    data_df['unilateral_loss'] = (((data_df['pta_l'] > 25) & (data_df['pta_r'] <= 25)) |
                                  ((data_df['pta_r'] > 25) & (data_df['pta_l'] <= 25))).astype(int)

    return data_df

def generate_clinical_summary(data_df: pd.DataFrame, prediction_result: dict) -> dict:
    """Generate clinical insights from the audiological data"""

    pta_l = data_df['pta_l'].iloc[0]
    pta_r = data_df['pta_r'].iloc[0]
    abg_avg_l = data_df['abg_avg_l'].iloc[0]
    abg_avg_r = data_df['abg_avg_r'].iloc[0]
    srt_pta_diff_l = data_df['srt_pta_diff_l'].iloc[0]
    srt_pta_diff_r = data_df['srt_pta_diff_r'].iloc[0]
    asymmetry = data_df['pta_asymmetry'].iloc[0]

    clinical_notes = []

    # PTA interpretation
    if pta_l <= 25 and pta_r <= 25:
        clinical_notes.append("Bilateral hearing within normal limits")
    elif pta_l > 25 and pta_r > 25:
        clinical_notes.append(f"Bilateral hearing loss (L: {pta_l:.0f} dB, R: {pta_r:.0f} dB)")
    else:
        clinical_notes.append(f"Unilateral hearing loss (L: {pta_l:.0f} dB, R: {pta_r:.0f} dB)")

    # Air-bone gap interpretation
    if abg_avg_l > 15 or abg_avg_r > 15:
        clinical_notes.append(f"Significant air-bone gaps present (L: {abg_avg_l:.0f} dB, R: {abg_avg_r:.0f} dB)")

    # SRT-PTA agreement
    if abs(srt_pta_diff_l) > 10 or abs(srt_pta_diff_r) > 10:
        clinical_notes.append("Poor SRT-PTA agreement suggests possible auditory neuropathy")

    # Asymmetry
    if asymmetry > 15:
        clinical_notes.append(f"Significant asymmetry ({asymmetry:.0f} dB) - consider retrocochlear pathology")

    # OAE status
    oae_present = (data_df['oae_500_present'].iloc[0] or
                   data_df['oae_1000_present'].iloc[0] or
                   data_df['oae_4000_present'].iloc[0])

    if prediction_result['hearing_loss'] == 'Yes' and oae_present:
        clinical_notes.append("OAEs present with hearing loss - suggests auditory neuropathy")

    return {
        'pta_left': round(pta_l, 1),
        'pta_right': round(pta_r, 1),
        'asymmetry': round(asymmetry, 1),
        'air_bone_gap_left': round(abg_avg_l, 1),
        'air_bone_gap_right': round(abg_avg_r, 1),
        'clinical_notes': clinical_notes
    }

@app.get("/")
def root():
    return {
        "message": "Hearing Loss Prediction API",
        "status": "Model loaded" if model is not None else "Model not loaded",
        "features": len(model_columns) if model_columns else 0
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None,
        "encoders_loaded": label_encoders is not None,
        "feature_count": len(model_columns) if model_columns else 0
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(request_data: PredictionRequest):
    """Predict hearing loss using comprehensive audiological assessment"""

    # Check if model is loaded
    if model is None or model_columns is None or label_encoders is None:
        raise HTTPException(
            status_code=500,
            detail="Model not loaded. Please check server logs and ensure training files are available."
        )

    try:
        # 1. Convert request to DataFrame
        data_dict = request_data.model_dump()
        data_df = pd.DataFrame([data_dict])

        logger.info(f"Processing prediction request for patient age {data_dict['age']}")

        # 2. Perform EXACT feature engineering as in training
        data_df = perform_feature_engineering(data_df)

        # 3. Handle categorical variables with one-hot encoding
        categorical_input_cols = ['tymp_type_l', 'tymp_type_r']
        data_df = pd.get_dummies(data_df, columns=categorical_input_cols, drop_first=False)

        # 4. Ensure all model columns are present (reindex to match training)
        data_df = data_df.reindex(columns=model_columns, fill_value=0)

        logger.info(f"Feature engineering complete. Shape: {data_df.shape}")

        # 5. Make prediction
        prediction_numeric = model.predict(data_df)
        prediction_proba = model.predict_proba(data_df)

        # 6. Decode predictions
        hearing_loss_pred = "Yes" if prediction_numeric[0][0] == 1 else "No"

        # Handle the encoded target variables
        loss_type_pred = label_encoders['hearing_loss_type'].inverse_transform([prediction_numeric[0][1]])[0]
        loss_severity_pred = label_encoders['hearing_loss_severity'].inverse_transform([prediction_numeric[0][2]])[0]

        # 7. Calculate confidence scores
        confidence_scores = {
            'hearing_loss': float(np.max(prediction_proba[0])),
            'hearing_loss_type': float(np.max(prediction_proba[1])),
            'hearing_loss_severity': float(np.max(prediction_proba[2]))
        }

        # 8. Generate clinical summary
        prediction_result = {
            'hearing_loss': hearing_loss_pred,
            'hearing_loss_type': loss_type_pred,
            'hearing_loss_severity': loss_severity_pred
        }

        clinical_summary = generate_clinical_summary(data_df, prediction_result)

        logger.info(f"Prediction complete: {hearing_loss_pred}, {loss_type_pred}, {loss_severity_pred}")

        # 9. Return comprehensive response
        return PredictionResponse(
            hearing_loss=hearing_loss_pred,
            hearing_loss_type=loss_type_pred,
            hearing_loss_severity=loss_severity_pred,
            confidence_scores=confidence_scores,
            clinical_summary=clinical_summary
        )

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/model-info")
def get_model_info():
    """Get information about the loaded model"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    info = {
        "model_type": "XGBoost MultiOutputClassifier",
        "total_features": len(model_columns) if model_columns else 0,
        "target_variables": list(label_encoders.keys()) if label_encoders else [],
        "feature_categories": {
            "audiometric": len([col for col in model_columns if any(x in col for x in ['ac_', 'bc_', 'srt_', 'wrs_'])]),
            "engineered": len([col for col in model_columns if any(x in col for x in ['abg_', 'pta_', 'hf_avg_'])]),
            "categorical": len([col for col in model_columns if 'tymp_type' in col]),
            "clinical_history": len([col for col in model_columns if any(x in col for x in ['age', 'sex', 'genetic', 'noise', 'tinnitus'])])
        } if model_columns else {}
    }

    # Add label encoder mappings
    if label_encoders:
        info["label_mappings"] = {}
        for key, encoder in label_encoders.items():
            info["label_mappings"][key] = {i: label for i, label in enumerate(encoder.classes_)}

    return info

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
