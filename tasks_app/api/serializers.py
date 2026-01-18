from rest_framework import serializers
from django.contrib.auth.models import User

from tasks_app.models import Task, Comments
from boards_app.models import Board
from user_auth_app.api.serializers import UserProfileSerializer


class TaskListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing and managing tasks.

    Supports assigning and reviewing users via IDs while returning
    detailed user profile data in responses.
    """

    board = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all(),
        help_text="Board ID the task belongs to."
    )

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source="assignee",
        required=False,
        allow_null=True,
        help_text="User ID assigned to the task."
    )

    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source="reviewer",
        required=False,
        allow_null=True,
        help_text="User ID reviewing the task."
    )

    assignee = UserProfileSerializer(
        read_only=True,
        help_text="Detailed profile of the assignee."
    )

    reviewer = UserProfileSerializer(
        read_only=True,
        help_text="Detailed profile of the reviewer."
    )

    comments_count = serializers.SerializerMethodField(
        help_text="Number of comments associated with the task."
    )

    def get_comments_count(self, obj):
        """
        Return the number of comments related to the task.
        """
        return obj.comments.count()

    class Meta:
        """
        Serializer metadata.
        """
        model = Task
        fields = [
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "assignee_id",
            "reviewer",
            "reviewer_id",
            "due_date",
            "comments_count",
        ]


class TaskNestedSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for embedding tasks in other responses.
    """

    assignee = UserProfileSerializer(read_only=True)
    reviewer = UserProfileSerializer(read_only=True)

    class Meta:
        """
        Serializer metadata.
        """
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
        ]


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for task comments.
    """

    class Meta:
        """
        Serializer metadata.
        """
        model = Comments
        fields = ["id", "created_at", "author", "content"]
        read_only_fields = ["id", "created_at", "author"]
