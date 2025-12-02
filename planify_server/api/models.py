from django.db import models
import secrets


class User(models.Model):
    name = models.CharField(max_length=100)
    email = model.EmailField(unique = true)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"


class AuthToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='token')
    key = models.CharField(max_length=64, unique=True,default=secrets.token_urlsafe)
    created_at = models.DateTimeField(auto_now_add=True)

    def regenerate(self):
        self.key = secrets.token_hex(32)
        self.save()
        return self.key


class Project (models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name='projects',blank=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATE_CHOICES = [
        ('todo', 'To Do'),
        ('doing', 'Doing'),
        ('done', 'Done'),
        ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='todo')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.project.name})"