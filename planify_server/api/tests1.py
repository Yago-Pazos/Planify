# planify_server/api/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from .models import User, AuthToken
from django.contrib.auth.hashers import check_password

import json

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_hash_and_login(self):
        # 1) register
        resp = self.client.post("/api/auth/register/", data=json.dumps({
            "name":"TestUser",
            "email":"testuser@example.com",
            "password":"secret123"
        }), content_type="application/json")
        self.assertIn(resp.status_code, (200,201))
        data = resp.json()
        self.assertIn("token", data)
        uid = data["id"]

        # 2) DB: password must be hashed (not equal to plaintext)
        u = User.objects.get(pk=uid)
        self.assertNotEqual(u.password, "secret123")
        self.assertTrue("$" in u.password)

        # 3) login with same credentials
        resp2 = self.client.post("/api/auth/login/", data=json.dumps({
            "email":"testuser@example.com",
            "password":"secret123"
        }), content_type="application/json")
        self.assertEqual(resp2.status_code, 200)
        data2 = resp2.json()
        self.assertIn("token", data2)

    def test_register_password_too_short(self):
        resp = self.client.post("/api/auth/register/", data=json.dumps({
            "name":"Short",
            "email":"short@example.com",
            "password":"123"
        }), content_type="application/json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Password", resp.json().get("error",""))

    def test_login_invalid_credentials(self):
        # try login for nonexistent user
        resp = self.client.post("/api/auth/login/", data=json.dumps({
            "email":"noone@example.com",
            "password":"whatever"
        }), content_type="application/json")
        self.assertEqual(resp.status_code, 401)
