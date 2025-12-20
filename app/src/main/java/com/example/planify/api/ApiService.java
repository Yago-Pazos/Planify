package com.tuapp.planify.api;

import com.example.planify.api.ApiConfig;

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
}
