from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Comments(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=70)
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.author} on {self.created_at}"


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'In Review'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    board = models.ForeignKey('boards_app.Board', related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    assignee = models.ManyToManyField(User, related_name="assigned_tasks", blank=True)
    reviewer = models.ManyToManyField(User, related_name='review_tasks', blank=True)
    due_date = models.DateField(null=True, blank=True)
    comments = models.ManyToManyField(Comments, related_name='comments_tasks', blank=True)


    def __str__(self):
        return self.title
    