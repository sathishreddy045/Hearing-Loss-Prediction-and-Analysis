package com.example.sathish.hearing_loss_backend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class PredictionRequest {
    // Demographics & History
    private int age;
    private int sex;

    @JsonProperty("genetic_history")
    private int geneticHistory;

    @JsonProperty("noise_exposure_history")
    private int noiseExposureHistory;

    private int tinnitus;

    @JsonProperty("vertigo_dizziness")
    private int vertigoDizziness;

    @JsonProperty("hearing_difficulty_in_noise")
    private int hearingDifficultyInNoise;

    // Left Ear Audiometry (these are correct)
    private double ac_l_250;
    private double ac_l_500;
    private double ac_l_1000;
    private double ac_l_2000;
    private double ac_l_4000;
    private double ac_l_8000;
    private double bc_l_500;
    private double bc_l_1000;
    private double bc_l_2000;
    private double bc_l_4000;
    private double srt_l;
    private double wrs_l;
    private String tymp_type_l;

    // Right Ear Audiometry (these are correct)
    private double ac_r_250;
    private double ac_r_500;
    private double ac_r_1000;
    private double ac_r_2000;
    private double ac_r_4000;
    private double ac_r_8000;
    private double bc_r_500;
    private double bc_r_1000;
    private double bc_r_2000;
    private double bc_r_4000;
    private double srt_r;
    private double wrs_r;
    private String tymp_type_r;

    // Optional Advanced Fields (with defaults matching Python)
    private int oae_500_present = 0;
    private int oae_1000_present = 0;
    private int oae_4000_present = 0;
    private double abr_wave_i_latency = 0.0;
    private double abr_wave_iii_latency = 0.0;
    private double abr_wave_v_latency = 0.0;
    private int abr_wave_v_absent = 0;
}