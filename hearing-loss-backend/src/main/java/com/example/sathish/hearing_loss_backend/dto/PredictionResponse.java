package com.example.sathish.hearing_loss_backend.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import java.util.Map;

@Data
public class PredictionResponse {
    @JsonProperty("hearing_loss")
    private String hearingLoss;

    @JsonProperty("hearing_loss_type")
    private String hearingLossType;

    @JsonProperty("hearing_loss_severity")
    private String hearingLossSeverity;

    @JsonProperty("confidence_scores")
    private ConfidenceScores confidenceScores;

    @JsonProperty("clinical_summary")
    private ClinicalSummary clinicalSummary;

    @Data
    public static class ConfidenceScores {
        @JsonProperty("hearing_loss")
        private double hearingLoss;

        @JsonProperty("hearing_loss_type")
        private double hearingLossType;

        @JsonProperty("hearing_loss_severity")
        private double hearingLossSeverity;
    }

    @Data
    public static class ClinicalSummary {
        @JsonProperty("pta_left")
        private double ptaLeft;

        @JsonProperty("pta_right")
        private double ptaRight;

        private double asymmetry;

        @JsonProperty("air_bone_gap_left")
        private double airBoneGapLeft;

        @JsonProperty("air_bone_gap_right")
        private double airBoneGapRight;

        @JsonProperty("clinical_notes")
        private java.util.List<String> clinicalNotes;
    }
}