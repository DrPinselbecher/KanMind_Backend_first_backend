from django.db import models
from django.contrib.auth.models import User


class Comments(models.Model):
    """
    Represents a comment attached to a task.

    A comment contains textual content, an author name,
    and a timestamp indicating when it was created.
    """

    task = models.ForeignKey(
        'tasks_app.Task',
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Task this comment belongs to."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the comment was created."
    )

    author = models.CharField(
        max_length=70,
        help_text="Name of the comment author."
    )

    content = models.TextField(
        help_text="Content of the comment."
    )

    def __str__(self):
        """
        Return a readable string representation of the comment.
        """
        return f"Comment by {self.author} on {self.created_at}"


class Task(models.Model):
    """
    Represents a task within a board.

    A task can be assigned, reviewed, prioritized,
    and moved through multiple workflow states.
    """

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

    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_tasks",
        help_text="User who created the task."
    )

    board = models.ForeignKey(
        'boards_app.Board',
        related_name='tasks',
        on_delete=models.CASCADE,
        help_text="Board this task belongs to."
    )

    title = models.CharField(
        max_length=255,
        help_text="Title of the task."
    )

    description = models.TextField(
        blank=True,
        help_text="Detailed description of the task."
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        help_text="Current workflow status of the task."
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        help_text="Priority level of the task."
    )

    assignee = models.ForeignKey(
        User,
        related_name="assigned_tasks",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="User assigned to work on the task."
    )

    reviewer = models.ForeignKey(
        User,
        related_name='review_tasks',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="User responsible for reviewing the task."
    )

    due_date = models.DateField(
        null=True,
        blank=True,
        help_text="Optional due date for the task."
    )

    def __str__(self):
        """
        Return the string representation of the task.
        """
        return self.title
