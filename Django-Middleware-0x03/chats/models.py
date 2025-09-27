from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"

# Extend User model with role
User.add_to_class('role', models.CharField(max_length=20, default='user', choices=[
    ('admin', 'Admin'),
    ('moderator', 'Moderator'),
    ('user', 'User')
]))