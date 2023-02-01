# models.py
from django.db import models

class AI(models.Model):
    name = models.CharField(max_length=100)
    profile = models.TextField()

    def __str__(self):
        return self.name

class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ai = models.ForeignKey(AI, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

