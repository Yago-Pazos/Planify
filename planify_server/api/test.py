from django.test import TestCase, Client
import json

class BackendTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_and_login(self):
        # Register
        response = self.client.post(
            "/api/auth/register/",
            data=json.dumps({
                "name": "Test User",
                "email": "test@example.com",
                "password": "password123"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        token = response.json().get("token")
        self.assertIsNotNone(token)

        # Login
        response = self.client.post(
            "/api/auth/login/",
            data=json.dumps({
                "email": "test@example.com",
                "password": "password123"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_project_creation(self):
        # Register user
        response = self.client.post(
            "/api/auth/register/",
            data=json.dumps({
                "name": "Project User",
                "email": "project@example.com",
                "password": "password123"
            }),
            content_type="application/json"
        )
        token = response.json()["token"]

        # Create project
        response = self.client.post(
            "/api/proyectos/",
            data=json.dumps({
                "name": "Proyecto Test",
                "description": "Descripción"
            }),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )
        self.assertEqual(response.status_code, 201)

    def test_task_creation(self):
        # Register
        response = self.client.post(
            "/api/auth/register/",
            data=json.dumps({
                "name": "Task User",
                "email": "task@example.com",
                "password": "password123"
            }),
            content_type="application/json"
        )
        token = response.json()["token"]

        # Create project
        response = self.client.post(
            "/api/proyectos/",
            data=json.dumps({
                "name": "Proyecto Tareas"
            }),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )
        project_id = response.json()["id"]

        # Create task
        response = self.client.post(
            f"/api/proyectos/{project_id}/tareas/",
            data=json.dumps({
                "title": "Tarea de prueba",
                "state": "todo"
            }),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )
        self.assertEqual(response.status_code, 201)
