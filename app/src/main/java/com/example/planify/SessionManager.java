package com.example.planify;

import android.content.Context;
import android.content.SharedPreferences;

public class SessionManager {

    private static final String PREF_NAME = "planify_session";
    private static final String KEY_LOGGED = "is_logged";
    private static final String KEY_EMAIL = "email";

    SharedPreferences prefs;
    SharedPreferences.Editor editor;

    public SessionManager(Context context) {
        prefs = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
        editor = prefs.edit();
    }

    public void login(String email) {
        editor.putBoolean(KEY_LOGGED, true);
        editor.putString(KEY_EMAIL, email);
        editor.apply();
    }

    public void logout() {
        editor.clear();
        editor.apply();
    }

    public boolean isLoggedIn() {
        return prefs.getBoolean(KEY_LOGGED, false);
    }

    public String getEmail() {
        return prefs.getString(KEY_EMAIL, null);
    }
}
