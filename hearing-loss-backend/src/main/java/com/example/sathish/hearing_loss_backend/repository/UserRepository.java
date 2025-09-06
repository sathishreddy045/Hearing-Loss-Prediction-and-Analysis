package com.example.sathish.hearing_loss_backend.repository;

import com.example.sathish.hearing_loss_backend.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    // We can define custom methods here. Spring Data JPA will implement them for us.
    Optional<User> findByEmail(String email);
}
