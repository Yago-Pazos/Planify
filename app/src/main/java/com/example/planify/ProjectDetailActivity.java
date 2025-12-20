package com.example.planify;

import android.app.Dialog;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class ProjectDetailActivity extends AppCompatActivity {

    // Layouts
    private View layoutBoard;
    private View layoutTeam;

    // Tabs
    private TextView tabBoard;
    private TextView tabTeam;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_project_detail);

        // Tabs
        tabBoard = findViewById(R.id.tabBoard);
        tabTeam = findViewById(R.id.tabTeam);

        // Layouts
        layoutBoard = findViewById(R.id.layoutBoard);
        layoutTeam = findViewById(R.id.layoutTeam);

        // Botones tareas
        Button btnNewTask = findViewById(R.id.btnNewTask);
        View btnAddTaskPending = findViewById(R.id.btnAddTaskPending);

        // Navegación de tabs
        tabBoard.setOnClickListener(v -> showBoard());
        tabTeam.setOnClickListener(v -> showTeam());

        // Abrir modal Nueva Tarea
        btnNewTask.setOnClickListener(v -> openNewTaskDialog());
        btnAddTaskPending.setOnClickListener(v -> openNewTaskDialog());

        // Estado inicial
        showBoard();
    }

    // ================= TABS =================

    private void showBoard() {
        layoutBoard.setVisibility(View.VISIBLE);
        layoutTeam.setVisibility(View.GONE);

        tabBoard.setTextColor(Color.parseColor("#5B4BEB"));
        tabBoard.setTypeface(null, Typeface.BOLD);

        tabTeam.setTextColor(Color.parseColor("#888888"));
        tabTeam.setTypeface(null, Typeface.NORMAL);
    }

    private void showTeam() {
        layoutBoard.setVisibility(View.GONE);
        layoutTeam.setVisibility(View.VISIBLE);

        tabTeam.setTextColor(Color.parseColor("#5B4BEB"));
        tabTeam.setTypeface(null, Typeface.BOLD);

        tabBoard.setTextColor(Color.parseColor("#888888"));
        tabBoard.setTypeface(null, Typeface.NORMAL);
    }

    // ================= MODAL NUEVA TAREA =================

    private void openNewTaskDialog() {
        Dialog dialog = new Dialog(this);
        dialog.setContentView(R.layout.dialog_new_task);

        if (dialog.getWindow() != null) {
            dialog.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
            dialog.getWindow().setLayout(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    ViewGroup.LayoutParams.WRAP_CONTENT
            );
        }

        ImageView btnClose = dialog.findViewById(R.id.btnClose);
        TextView btnCancel = dialog.findViewById(R.id.btnCancel);
        Button btnSave = dialog.findViewById(R.id.btnSaveTask);

        EditText etTitle = dialog.findViewById(R.id.etTitle);
        EditText etDescription = dialog.findViewById(R.id.etDescription);

        btnClose.setOnClickListener(v -> dialog.dismiss());
        btnCancel.setOnClickListener(v -> dialog.dismiss());

        btnSave.setOnClickListener(v -> {
            String title = etTitle.getText().toString().trim();
            String description = etDescription.getText().toString().trim();

            if (!title.isEmpty()) {
                addTaskToPending(title, description);
                dialog.dismiss();
            }
        });

        dialog.show();
    }

    // ================= AÑADIR TAREA VISUAL =================

    private void addTaskToPending(String title, String description) {
        LinearLayout container = findViewById(R.id.containerPendingTasks);

        LinearLayout card = new LinearLayout(this);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setPadding(24, 16, 24, 16);
        card.setBackgroundResource(R.drawable.card_background);

        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
        );
        params.setMargins(0, 0, 0, 12);
        card.setLayoutParams(params);

        TextView tvTitle = new TextView(this);
        tvTitle.setText(title);
        tvTitle.setTextSize(14);
        tvTitle.setTypeface(null, Typeface.BOLD);

        TextView tvDesc = new TextView(this);
        tvDesc.setText(description);
        tvDesc.setTextColor(Color.GRAY);
        tvDesc.setTextSize(12);

        card.addView(tvTitle);
        card.addView(tvDesc);

        container.addView(card, 0);
    }
}
