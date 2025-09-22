from django.conf import settings
from django.db import models
from tasks_app.models import Task

class Board(models.Model):
    title = models.CharField(max_length=255)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='boards',
        blank=True
    )
    tasks = models.ManyToManyField(
        Task,
        related_name='boards',
        blank=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='owned_boards',
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.members.add(self.owner)

    def __str__(self):
        return self.title
