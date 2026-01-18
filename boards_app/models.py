from django.conf import settings
from django.db import models


class Board(models.Model):
    """
    Represents a board used to organize tasks and members.

    A board has an owner and can contain multiple members.
    The owner is automatically added as a member when the board is created.
    """

    title = models.CharField(
        max_length=255,
        help_text="Title of the board."
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='boards',
        blank=True,
        help_text="Users who are members of this board."
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='owned_boards',
        on_delete=models.CASCADE,
        help_text="User who owns the board."
    )

    class Meta:
        """
        Model metadata.
        """
        ordering = ["title"]

    def save(self, *args, **kwargs):
        """
        Save the board instance.

        Automatically adds the owner to the members list
        when the board is created for the first time.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            self.members.add(self.owner)

    def __str__(self):
        """
        Return the string representation of the board.
        """
        return self.title
