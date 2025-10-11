from rest_framework import serializers
from django.contrib.auth.models import User

from tasks_app.models import Task
from boards_app.models import Board
from user_auth_app.api.serializers import UserProfileSerializer

class TaskListSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())

    assignee_id = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        source="assignee"
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        source="reviewer"
    )

    assignee = UserProfileSerializer(many=True, read_only=True)
    reviewer = UserProfileSerializer(many=True, read_only=True)


    def create(self, validated_data):
        assignees = validated_data.pop('assignee', [])
        reviewers = validated_data.pop('reviewer', [])
        task = Task.objects.create(**validated_data)
        task.assignee.set(assignees)
        task.reviewer.set(reviewers)
        return task

    class Meta:
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
        ]

class TaskNestedSerializer(serializers.ModelSerializer):
    assignee = UserProfileSerializer(many=True, read_only=True)
    reviewer = UserProfileSerializer(many=True, read_only=True)

    class Meta:
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

class TaskDetailSerializer(serializers.ModelSerializer):
    pass