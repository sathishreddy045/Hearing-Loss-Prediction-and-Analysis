package com.example.sathish.hearing_loss_backend.service;


import com.example.sathish.hearing_loss_backend.dto.PredictionRequest;
import com.example.sathish.hearing_loss_backend.dto.PredictionResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class PredictionService {

    // The RestTemplate is Spring's primary tool for making HTTP requests.
    private final RestTemplate restTemplate;

    // This will read the URL of our Python service from application.properties
    @Value("${ml.model.url}")
    private String mlModelUrl;

    public PredictionService() {
        this.restTemplate = new RestTemplate();
    }

    public PredictionResponse getPrediction(PredictionRequest request) {
        // Make a POST request to the Python Flask service's /predict endpoint,
        // sending the patient data and expecting a PredictionResponse back.
        return restTemplate.postForObject(mlModelUrl, request, PredictionResponse.class);
    }
}
