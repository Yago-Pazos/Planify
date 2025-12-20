package com.example.planify;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import androidx.appcompat.app.AppCompatActivity;

public class HomeActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        View cardProject = findViewById(R.id.cardProject);
        Button btnNewProject = findViewById(R.id.btnNewProject);
        ImageView btnLogout = findViewById(R.id.btnLogout);

        cardProject.setOnClickListener(v ->
                startActivity(new Intent(this, ProjectDetailActivity.class))
        );

        btnNewProject.setOnClickListener(v -> {
            // luego abriremos el dialog_create_project
        });

        btnLogout.setOnClickListener(v -> {
            startActivity(new Intent(this, MainActivity.class));
            finish();
        });
    }
}
