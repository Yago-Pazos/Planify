package com.example.planify;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import androidx.appcompat.app.AppCompatActivity;

public class HomeActivity extends AppCompatActivity {

    SessionManager session;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        // 🔹 Inicializar sesión
        session = new SessionManager(this);

        // 🔹 Proteger Home
        if (!session.isLoggedIn()) {
            startActivity(new Intent(this, LoginActivity.class));
            finish();
            return;
        }

        // 🔹 Views
        ImageView btnLogout = findViewById(R.id.btnLogout);
        View cardProject = findViewById(R.id.cardProject);
        Button btnNewProject = findViewById(R.id.btnNewProject);

        // 🔹 Logout
        btnLogout.setOnClickListener(v -> {
            session.logout();
            startActivity(new Intent(this, LoginActivity.class));
            finish();
        });

        // 🔹 Ir a detalle de proyecto
        cardProject.setOnClickListener(v ->
                startActivity(new Intent(this, ProjectDetailActivity.class))
        );

        // 🔹 Nuevo proyecto (luego)
        btnNewProject.setOnClickListener(v -> {
            // aquí abrirás el diálogo de crear proyecto
        });
    }
}
