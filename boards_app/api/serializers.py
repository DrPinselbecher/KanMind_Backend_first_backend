from rest_framework import serializers
from django.contrib.auth.models import User

from boards_app.models import Board
from user_auth_app.api.serializers import UserProfileSerializer
from tasks_app.api.serializers import TaskNestedSerializer


class BoardListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing and creating boards.

    Includes aggregated counts and supports assigning members
    via primary key references on creation.
    """

    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        help_text="User IDs to be added as board members."
    )

    member_count = serializers.IntegerField(read_only=True)
    ticket_count = serializers.IntegerField(read_only=True)
    tasks_to_do_count = serializers.IntegerField(read_only=True)
    tasks_high_prio_count = serializers.IntegerField(read_only=True)
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

    def create(self, validated_data):
        """
        Create a board and assign members.

        The owner is automatically added to the members list.
        """
        members = validated_data.pop('members', [])
        board = Board.objects.create(**validated_data)

        board.members.set(members)
        board.members.add(board.owner)

        return board

    class Meta:
        """
        Serializer metadata.
        """
        model = Board
        fields = [
            "id",
            "title",
            "members",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
        ]


class BoardDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving a single board with full details.

    Includes nested members and tasks.
    """

    members = UserProfileSerializer(many=True, read_only=True)
    tasks = TaskNestedSerializer(many=True, read_only=True)
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

    class Meta:
        """
        Serializer metadata.
        """
        model = Board
        fields = [
            "id",
            "title",
            "members",
            "owner_id",
            "tasks",
        ]


class BoardUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating boards.

    Allows updating members via IDs while returning
    detailed owner and member information.
    """

    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        help_text="User IDs to update board members."
    )

    owner_data = UserProfileSerializer(
        source="owner",
        read_only=True
    )

    members_data = UserProfileSerializer(
        source="members",
        many=True,
        read_only=True
    )

    class Meta:
        """
        Serializer metadata.
        """
        model = Board
        fields = [
            "id",
            "title",
            "owner_data",
            "members_data",
            "members",
        ]
