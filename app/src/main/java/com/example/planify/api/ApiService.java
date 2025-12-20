package com.example.planify.api;

import android.util.Log;

import org.json.JSONArray;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;

public class ApiService {

    public static JSONArray getProjects() throws Exception {
        URL url = new URL(ApiConfig.BASE_URL + "proyectos/");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        conn.setRequestProperty("Accept", "application/json");

        BufferedReader reader = new BufferedReader(
                new InputStreamReader(conn.getInputStream())
        );

        StringBuilder result = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            result.append(line);
        }

        return new JSONArray(result.toString());
    }
    public static void createProject(String title, String description) throws Exception {
        URL url = new URL(ApiConfig.BASE_URL + "proyectos/");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();

        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);

        String json = "{"
                + "\"name\":\"" + title + "\","
                + "\"description\":\"" + description + "\""
                + "}";

        OutputStream os = conn.getOutputStream();
        os.write(json.getBytes());
        os.close();

        conn.getResponseCode(); // fuerza envío
    }

    public static boolean login(String username, String password) throws Exception {
        URL url = new URL(ApiConfig.BASE_URL + "auth/login/");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();

        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);

        String json = "{"
                + "\"email\":\"" + username + "\","
                + "\"password\":\"" + password + "\""
                + "}";


        OutputStream os = conn.getOutputStream();
        os.write(json.getBytes());
        os.close();

        int responseCode = conn.getResponseCode();
        Log.d("LOGIN_HTTP", "Código HTTP: " + responseCode);

        return responseCode == 200;
    }

    public static boolean register(String name, String email, String password) throws Exception {
        URL url = new URL(ApiConfig.BASE_URL + "auth/register/");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();

        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);

        String json = "{"
                + "\"name\":\"" + name + "\","
                + "\"email\":\"" + email + "\","
                + "\"password\":\"" + password + "\""
                + "}";

        OutputStream os = conn.getOutputStream();
        os.write(json.getBytes());
        os.close();

        int responseCode = conn.getResponseCode();
        return responseCode == 201;
    }






}
