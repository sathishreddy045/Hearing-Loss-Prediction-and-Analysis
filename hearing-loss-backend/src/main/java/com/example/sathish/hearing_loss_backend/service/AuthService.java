// src/main/java/com/audiology/hearinglossapi/service/AuthService.java
package com.example.sathish.hearing_loss_backend.service;

import com.example.sathish.hearing_loss_backend.model.User;
import com.example.sathish.hearing_loss_backend.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    @Autowired
    private UserRepository userRepository;

    // We need to configure a PasswordEncoder Bean for this to be injected
    // For now, let's assume it's configured elsewhere.
    @Autowired
    private PasswordEncoder passwordEncoder;

    public User signup(String email, String fullName, String password) {
        // Check if user already exists
        if (userRepository.findByEmail(email).isPresent()) {
            throw new RuntimeException("Error: Email is already in use!");
        }

        // Create new user's account
        // We should encrypt the password before saving
        String encodedPassword = passwordEncoder.encode(password);
        User user = new User(email, fullName, encodedPassword);

        return userRepository.save(user);
    }
}
