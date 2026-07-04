from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

    STATUS_CHOICES = [
        ("To do", "todo"),
        ("In progress", "in_progress"),
        ("Done", "done"),
    ]

    PRIORITY_CHOICES = [
        ("Low", "low"),
        ("Medium", "medium"),
        ("High", "high"),
        ("Critical High", "critical_high"),
    ]


    title = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="todo")
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default="low")
    due_date = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to='comments_media/', null=True, blank=True)