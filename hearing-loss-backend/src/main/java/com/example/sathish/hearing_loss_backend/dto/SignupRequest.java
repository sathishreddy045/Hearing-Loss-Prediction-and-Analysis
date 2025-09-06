package com.example.sathish.hearing_loss_backend.dto;

import lombok.Data;

@Data
public class SignupRequest {
    public String email;
    public String fullName;
    public String password;
}

