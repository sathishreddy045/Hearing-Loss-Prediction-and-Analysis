package com.example.sathish.hearing_loss_backend.controller;

import com.example.sathish.hearing_loss_backend.dto.PredictionRequest;
import com.example.sathish.hearing_loss_backend.dto.PredictionResponse;
import com.example.sathish.hearing_loss_backend.service.PredictionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class PredictionController {

    @Autowired
    private PredictionService predictionService;

    @PostMapping("/predict")
    public ResponseEntity<PredictionResponse> predictHearingLoss(@RequestBody PredictionRequest request) {
        try {
            PredictionResponse response = predictionService.getPrediction(request);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            // Handle cases where the Python service might be down or return an error
            return ResponseEntity.internalServerError().build();
        }
    }
}
