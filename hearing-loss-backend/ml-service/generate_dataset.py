import csv
import random
import numpy as np
from typing import Dict, Tuple, List

# --- Configuration ---
NUM_RECORDS = 550
OUTPUT_FILE = 'synthetic_hearing_loss_data.csv'

FIELDNAMES = [
    'age', 'sex', 'genetic_history', 'tinnitus', 'vertigo_dizziness',
    'noise_exposure_history', 'hearing_difficulty_in_noise',
    'ac_l_250', 'ac_l_500', 'ac_l_1000', 'ac_l_2000', 'ac_l_4000', 'ac_l_8000',
    'bc_l_500', 'bc_l_1000', 'bc_l_2000', 'bc_l_4000', 'srt_l', 'wrs_l', 'tymp_type_l',
    'ac_r_250', 'ac_r_500', 'ac_r_1000', 'ac_r_2000', 'ac_r_4000', 'ac_r_8000',
    'bc_r_500', 'bc_r_1000', 'bc_r_2000', 'bc_r_4000', 'srt_r', 'wrs_r', 'tymp_type_r',
    'oae_500_present', 'oae_1000_present', 'oae_4000_present',
    'abr_wave_i_latency', 'abr_wave_iii_latency', 'abr_wave_v_latency', 'abr_wave_v_absent',
    'hearing_loss', 'hearing_loss_type', 'hearing_loss_severity'
]

def clamp(value: float, min_val: float = -10, max_val: float = 120) -> int:
    """Clamp audiometric values to realistic ranges"""
    return int(max(min_val, min(max_val, value)))

def add_presbycusis(ac_thresholds: Dict[int, int], age: int) -> Dict[int, int]:
    """Add age-related hearing loss pattern"""
    if age < 40:
        return ac_thresholds

    # Presbycusis affects high frequencies more
    age_factor = (age - 40) / 60.0  # Scale factor from 40-100 years
    presbycusis_loss = {
        250: age_factor * random.randint(0, 5),
        500: age_factor * random.randint(0, 10),
        1000: age_factor * random.randint(5, 15),
        2000: age_factor * random.randint(10, 25),
        4000: age_factor * random.randint(20, 40),
        8000: age_factor * random.randint(30, 50)
    }

    for freq in ac_thresholds:
        ac_thresholds[freq] += int(presbycusis_loss[freq])
        ac_thresholds[freq] = clamp(ac_thresholds[freq])

    return ac_thresholds

def generate_ear_data(profile: str = 'normal', age: int = 30, noise_exposure: bool = False) -> Dict:
    """Generates audiological data for a single ear with improved realism"""
    ear = {}
    ac = {}
    bc = {}

    if profile == 'normal':
        # Normal hearing with slight variability
        ac = {hz: random.randint(-5, 15) for hz in [250, 500, 1000, 2000, 4000, 8000]}
        bc = {hz: ac[hz] - random.randint(0, 5) for hz in [500, 1000, 2000, 4000]}

    elif profile == 'snhl':
        # More realistic SNHL patterns
        if noise_exposure and age > 20:
            # Noise-induced pattern (4kHz notch)
            base_loss = random.randint(15, 35)
            ac = {
                250: base_loss + random.randint(-5, 5),
                500: base_loss + random.randint(-5, 5),
                1000: base_loss + random.randint(0, 10),
                2000: base_loss + random.randint(5, 15),
                4000: base_loss + random.randint(25, 45),  # Characteristic 4kHz dip
                8000: base_loss + random.randint(15, 35)
            }
        else:
            # Gradual sloping SNHL
            base_loss = random.randint(20, 45)
            slope_factor = random.uniform(0.8, 1.5)
            ac = {
                250: int(base_loss * 0.6 + random.randint(-5, 5)),
                500: int(base_loss * 0.7 + random.randint(-5, 5)),
                1000: int(base_loss * 0.9 + random.randint(-5, 5)),
                2000: int(base_loss * slope_factor + random.randint(-5, 5)),
                4000: int(base_loss * (slope_factor + 0.4) + random.randint(-5, 10)),
                8000: int(base_loss * (slope_factor + 0.6) + random.randint(-5, 15))
            }

        # SNHL: minimal air-bone gap
        bc = {hz: ac[hz] - random.randint(0, 10) for hz in [500, 1000, 2000, 4000]}

    elif profile == 'conductive':
        # More realistic conductive loss with consistent air-bone gaps
        bc_levels = {hz: random.randint(5, 20) for hz in [500, 1000, 2000, 4000]}
        air_bone_gap = random.randint(20, 45)  # Consistent gap
        ac = {
            250: bc_levels[500] + air_bone_gap + random.randint(-5, 5),
            500: bc_levels[500] + air_bone_gap + random.randint(-5, 5),
            1000: bc_levels[1000] + air_bone_gap + random.randint(-5, 5),
            2000: bc_levels[2000] + air_bone_gap + random.randint(-5, 5),
            4000: bc_levels[4000] + air_bone_gap + random.randint(-5, 5),
            8000: bc_levels[4000] + air_bone_gap + random.randint(-5, 10)
        }
        bc = bc_levels

    elif profile == 'mixed':
        # Mixed hearing loss: SNHL + conductive component
        snhl_component = random.randint(25, 45)
        conductive_component = random.randint(15, 30)

        bc = {hz: snhl_component + random.randint(-5, 5) for hz in [500, 1000, 2000, 4000]}
        ac = {
            250: bc[500] + conductive_component + random.randint(-5, 5),
            500: bc[500] + conductive_component + random.randint(-5, 5),
            1000: bc[1000] + conductive_component + random.randint(-5, 5),
            2000: bc[2000] + conductive_component + random.randint(-5, 5),
            4000: bc[4000] + conductive_component + random.randint(-5, 5),
            8000: bc[4000] + conductive_component + random.randint(-5, 10)  # Use 4kHz BC for 8kHz estimate
        }

    elif profile == 'ansd':
        # ANSD: variable hearing levels, often better at low frequencies
        low_freq_loss = random.randint(15, 40)
        high_freq_loss = random.randint(25, 65)
        ac = {
            250: low_freq_loss + random.randint(-10, 10),
            500: low_freq_loss + random.randint(-5, 10),
            1000: int((low_freq_loss + high_freq_loss) / 2) + random.randint(-10, 10),
            2000: high_freq_loss + random.randint(-10, 10),
            4000: high_freq_loss + random.randint(-5, 15),
            8000: high_freq_loss + random.randint(0, 20)
        }
        bc = {hz: ac[hz] - random.randint(0, 10) for hz in [500, 1000, 2000, 4000]}

    elif profile == 'unilateral':
        # Unilateral profound loss (sudden or acoustic neuroma)
        ac = {hz: random.randint(85, 120) for hz in [250, 500, 1000, 2000, 4000, 8000]}
        bc = {hz: random.randint(80, 120) for hz in [500, 1000, 2000, 4000]}

    # Apply presbycusis if age warrants it
    if age >= 40 and profile in ['normal', 'snhl', 'mixed']:
        ac = add_presbycusis(ac, age)

    # Clamp all values to realistic ranges
    for freq in ac: ac[freq] = clamp(ac[freq])
    for freq in bc: bc[freq] = clamp(bc[freq])

    # Calculate PTA and derived measures
    pta_freqs = [500, 1000, 2000, 4000]
    pta = np.mean([ac[freq] for freq in pta_freqs])

    # SRT calculation with profile-specific adjustments
    if profile == 'ansd':
        ear['srt'] = clamp(pta + random.randint(10, 25))  # Poor SRT-PTA agreement
    elif profile == 'conductive':
        ear['srt'] = clamp(pta + random.randint(-3, 3))   # Good agreement
    else:
        ear['srt'] = clamp(pta + random.randint(-5, 5))   # Typical variability

    # Word Recognition Score based on profile and severity
    if profile == 'ansd':
        ear['wrs'] = random.randint(10, 60)  # Characteristically poor
    elif profile == 'conductive':
        ear['wrs'] = random.randint(88, 100)  # Excellent with adequate volume
    elif pta <= 25:
        ear['wrs'] = random.randint(92, 100)
    elif pta <= 55:
        ear['wrs'] = random.randint(72, 96)
    elif pta <= 80:
        ear['wrs'] = random.randint(40, 80)
    else:
        ear['wrs'] = random.randint(0, 50)

    # Tympanometry
    if profile == 'conductive':
        ear['tymp_type'] = random.choices(['B', 'C', 'As'], weights=[0.5, 0.3, 0.2])[0]
    elif profile == 'mixed':
        ear['tymp_type'] = random.choices(['A', 'As', 'C'], weights=[0.4, 0.3, 0.3])[0]
    else:
        ear['tymp_type'] = random.choices(['A', 'As', 'Ad'], weights=[0.8, 0.15, 0.05])[0]

    # Flatten the data structure - don't add frequency to key names here
    ear['ac_thresholds'] = ac
    ear['bc_thresholds'] = bc

    return ear, pta

def determine_hearing_profiles(age: int, genetic_history: bool, noise_exposure: bool) -> Tuple[str, str]:
    """Determine hearing loss profiles for both ears based on risk factors"""

    # Base probabilities
    if age < 18:
        if genetic_history:
            profiles = ['normal', 'snhl', 'conductive', 'ansd', 'unilateral']
            weights = [0.3, 0.3, 0.2, 0.15, 0.05]
        else:
            profiles = ['normal', 'conductive', 'snhl', 'ansd']
            weights = [0.7, 0.2, 0.08, 0.02]
    elif age < 40:
        if noise_exposure:
            profiles = ['normal', 'snhl', 'conductive', 'mixed', 'unilateral']
            weights = [0.4, 0.45, 0.08, 0.05, 0.02]
        else:
            profiles = ['normal', 'snhl', 'conductive', 'ansd', 'unilateral']
            weights = [0.65, 0.2, 0.1, 0.03, 0.02]
    elif age < 65:
        profiles = ['normal', 'snhl', 'conductive', 'mixed', 'unilateral']
        weights = [0.3, 0.5, 0.1, 0.08, 0.02]
    else:  # 65+
        profiles = ['normal', 'snhl', 'mixed', 'conductive', 'unilateral']
        weights = [0.15, 0.65, 0.12, 0.06, 0.02]

    profile_l = random.choices(profiles, weights=weights)[0]

    # Determine if bilateral or unilateral
    if profile_l == 'unilateral':
        profile_r = 'normal'
    elif profile_l in ['snhl', 'mixed'] and age > 50:
        # Higher chance of bilateral age-related loss
        profile_r = random.choices([profile_l, 'normal'], weights=[0.7, 0.3])[0]
    elif profile_l == 'conductive':
        # Conductive losses often unilateral
        profile_r = random.choices([profile_l, 'normal'], weights=[0.3, 0.7])[0]
    else:
        # Most other cases
        profile_r = random.choices([profile_l, 'normal'], weights=[0.4, 0.6])[0]

    return profile_l, profile_r

def generate_patient_record() -> Dict:
    """Generate a complete patient record with improved clinical realism"""
    age = random.randint(0, 100)
    sex = random.choice([0, 1])

    # Risk factors with age-appropriate probabilities
    if age < 18:
        genetic_history = random.choices([0, 1], weights=[0.85, 0.15])[0]
        noise_exposure_history = random.choices([0, 1], weights=[0.9, 0.1])[0]
    elif age < 40:
        genetic_history = random.choices([0, 1], weights=[0.9, 0.1])[0]
        noise_exposure_history = random.choices([0, 1], weights=[0.6, 0.4])[0]
    else:
        genetic_history = random.choices([0, 1], weights=[0.95, 0.05])[0]
        noise_exposure_history = random.choices([0, 1], weights=[0.4, 0.6])[0]

    patient = {
        'age': age,
        'sex': sex,
        'genetic_history': genetic_history,
        'vertigo_dizziness': random.choices([0, 1], weights=[0.9, 0.1])[0],
        'noise_exposure_history': noise_exposure_history,
    }

    # Determine hearing profiles
    profile_l, profile_r = determine_hearing_profiles(age, genetic_history, noise_exposure_history)

    # Generate ear-specific data
    data_l, pta_l = generate_ear_data(profile_l, age, noise_exposure_history)
    data_r, pta_r = generate_ear_data(profile_r, age, noise_exposure_history)

    # Add ear data to patient record in the correct format
    for freq in [250, 500, 1000, 2000, 4000, 8000]:
        patient[f'ac_l_{freq}'] = data_l['ac_thresholds'][freq]
        patient[f'ac_r_{freq}'] = data_r['ac_thresholds'][freq]

    for freq in [500, 1000, 2000, 4000]:
        patient[f'bc_l_{freq}'] = data_l['bc_thresholds'][freq]
        patient[f'bc_r_{freq}'] = data_r['bc_thresholds'][freq]

    # Add other ear-specific data
    for key in ['srt', 'wrs', 'tymp_type']:
        patient[f'{key}_l'] = data_l[key]
        patient[f'{key}_r'] = data_r[key]

    # Determine tinnitus and hearing difficulty based on actual hearing loss
    worse_pta = max(pta_l, pta_r)
    if worse_pta > 25:
        # Higher probability of tinnitus and difficulty with hearing loss
        patient['tinnitus'] = random.choices([0, 1], weights=[0.3, 0.7])[0]
        patient['hearing_difficulty_in_noise'] = random.choices([0, 1], weights=[0.2, 0.8])[0]
    else:
        # Normal hearing - lower probability
        patient['tinnitus'] = random.choices([0, 1], weights=[0.85, 0.15])[0]
        patient['hearing_difficulty_in_noise'] = random.choices([0, 1], weights=[0.9, 0.1])[0]

    # Overall hearing loss classification
    if worse_pta <= 25 and profile_l == 'normal' and profile_r == 'normal':
        patient['hearing_loss'] = 0
        patient['hearing_loss_type'] = 'Normal'
        patient['hearing_loss_severity'] = 'Normal'
    else:
        patient['hearing_loss'] = 1

        # Determine primary type (based on worse ear or bilateral pattern)
        if profile_l == 'ansd' or profile_r == 'ansd':
            patient['hearing_loss_type'] = 'Auditory Neuropathy'
        elif profile_l == 'mixed' or profile_r == 'mixed':
            patient['hearing_loss_type'] = 'Mixed'
        elif profile_l == 'conductive' or profile_r == 'conductive':
            if (profile_l == 'conductive' and profile_r == 'normal') or \
                    (profile_l == 'normal' and profile_r == 'conductive'):
                patient['hearing_loss_type'] = 'Conductive'
            else:
                patient['hearing_loss_type'] = 'Conductive'
        else:
            patient['hearing_loss_type'] = 'Sensorineural'

        # Severity based on better ear (except for unilateral losses)
        if profile_l == 'unilateral' or profile_r == 'unilateral':
            better_pta = min(pta_l, pta_r)
            severity_pta = better_pta if better_pta <= 25 else worse_pta
        else:
            severity_pta = worse_pta

        if severity_pta <= 40:
            patient['hearing_loss_severity'] = 'Mild'
        elif severity_pta <= 70:
            patient['hearing_loss_severity'] = 'Moderate'
        elif severity_pta <= 90:
            patient['hearing_loss_severity'] = 'Severe'
        else:
            patient['hearing_loss_severity'] = 'Profound'

    # Advanced diagnostic test results
    is_ansd = patient['hearing_loss_type'] == 'Auditory Neuropathy'
    has_snhl = patient['hearing_loss_type'] in ['Sensorineural', 'Mixed', 'Auditory Neuropathy']
    is_normal = patient['hearing_loss_type'] == 'Normal'

    # OAEs: Present in normal hearing and ANSD, absent in cochlear pathology
    if is_normal or worse_pta <= 25:
        oae_present = 1
    elif is_ansd:
        oae_present = 1  # Characteristic finding
    elif has_snhl and worse_pta > 40:
        oae_present = 0  # Absent with significant cochlear damage
    else:
        oae_present = random.choices([0, 1], weights=[0.7, 0.3])[0]

    patient.update({
        'oae_500_present': oae_present,
        'oae_1000_present': oae_present,
        'oae_4000_present': oae_present,
    })

    # ABR results
    if is_ansd:
        # ANSD: Absent or severely abnormal waves
        patient.update({
            'abr_wave_i_latency': 0,  # Often absent
            'abr_wave_iii_latency': 0,  # Often absent
            'abr_wave_v_latency': 0,  # Often absent
            'abr_wave_v_absent': 1,
        })
    elif worse_pta > 70:
        # Severe/profound loss: May have absent responses
        patient.update({
            'abr_wave_i_latency': 0,
            'abr_wave_iii_latency': 0,
            'abr_wave_v_latency': 0,
            'abr_wave_v_absent': 1,
        })
    else:
        # Normal or mild-moderate loss: Present but possibly delayed
        delay_factor = max(0, (worse_pta - 20) / 50)  # Delay increases with severity
        patient.update({
            'abr_wave_i_latency': round(random.uniform(1.5, 1.8) + delay_factor * 0.3, 2),
            'abr_wave_iii_latency': round(random.uniform(3.5, 3.9) + delay_factor * 0.4, 2),
            'abr_wave_v_latency': round(random.uniform(5.5, 5.8) + delay_factor * 0.5, 2),
            'abr_wave_v_absent': 0,
        })

    return patient

# --- Main Generation Logic ---
if __name__ == "__main__":
    print(f"Generating {NUM_RECORDS} synthetic hearing loss records...")

    all_data = []
    for i in range(NUM_RECORDS):
        if (i + 1) % 50 == 0:
            print(f"Generated {i + 1}/{NUM_RECORDS} records...")
        all_data.append(generate_patient_record())

    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(all_data)

    print(f"\n✅ Successfully generated {len(all_data)} records in '{OUTPUT_FILE}'")

    # Quick statistics
    hearing_loss_count = sum(1 for record in all_data if record['hearing_loss'] == 1)
    print(f"📊 Statistics:")
    print(f"   - Normal hearing: {NUM_RECORDS - hearing_loss_count} ({100*(NUM_RECORDS - hearing_loss_count)/NUM_RECORDS:.1f}%)")
    print(f"   - Hearing loss: {hearing_loss_count} ({100*hearing_loss_count/NUM_RECORDS:.1f}%)")

    # Type distribution
    type_counts = {}
    for record in all_data:
        hl_type = record['hearing_loss_type']
        type_counts[hl_type] = type_counts.get(hl_type, 0) + 1

    print(f"   - Type distribution:")
    for hl_type, count in sorted(type_counts.items()):
        print(f"     • {hl_type}: {count} ({100*count/NUM_RECORDS:.1f}%)")