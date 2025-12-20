package com.example.planify;

import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.planify.api.ApiService;

public class RegisterActivity extends AppCompatActivity {

    EditText etName, etEmail, etPassword;
    Button btnRegister;
    TextView tvGoToLogin;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        etName = findViewById(R.id.etName);
        etEmail = findViewById(R.id.etEmail);
        etPassword = findViewById(R.id.etPassword);
        btnRegister = findViewById(R.id.btnRegister);
        tvGoToLogin = findViewById(R.id.tvGoToLogin);

        btnRegister.setOnClickListener(v -> {

            // 🔹 AHORA SÍ leemos el nombre
            String name = etName.getText().toString().trim();
            String email = etEmail.getText().toString().trim();
            String password = etPassword.getText().toString().trim();

            if (name.isEmpty() || email.isEmpty() || password.isEmpty()) {
                Toast.makeText(this, "Rellena todos los campos", Toast.LENGTH_SHORT).show();
                return;
            }

            new Thread(() -> {
                try {
                    // 🔹 AHORA mandamos name + email + password
                    boolean success = ApiService.register(name, email, password);

                    runOnUiThread(() -> {
                        if (success) {
                            Toast.makeText(this, "Usuario creado correctamente", Toast.LENGTH_SHORT).show();
                            finish(); // vuelve al login
                        } else {
                            Toast.makeText(this, "No se pudo crear el usuario", Toast.LENGTH_SHORT).show();
                        }
                    });

                } catch (Exception e) {
                    runOnUiThread(() ->
                            Toast.makeText(this, "Error de conexión", Toast.LENGTH_SHORT).show()
                    );
                }
            }).start();
        });

        tvGoToLogin.setOnClickListener(v -> finish());
    }
}
