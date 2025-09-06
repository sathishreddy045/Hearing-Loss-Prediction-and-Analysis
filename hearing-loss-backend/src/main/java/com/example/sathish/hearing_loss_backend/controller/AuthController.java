package com.example.sathish.hearing_loss_backend.controller;

import com.example.sathish.hearing_loss_backend.dto.SignupRequest;
import com.example.sathish.hearing_loss_backend.dto.UserDto;
import com.example.sathish.hearing_loss_backend.model.User;
import com.example.sathish.hearing_loss_backend.service.AuthService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AuthService authService;

    @PostMapping("/signup")
    public ResponseEntity<?> signupUser(@RequestBody SignupRequest signupRequest) {
        try {
            User newUser = authService.signup(signupRequest.email, signupRequest.fullName, signupRequest.password);
            return new ResponseEntity<>(new UserDto(newUser.getId(), newUser.getFullName(), newUser.getEmail()), HttpStatus.CREATED);
        } catch (RuntimeException e) {
            return new ResponseEntity<>(e.getMessage(), HttpStatus.BAD_REQUEST);
        }
    }

    // The /login and /logout endpoints are now handled automatically by Spring Security's formLogin()
}
