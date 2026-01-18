# third party imports
from django.db.models import Count, Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404

# local imports
from boards_app.models import Board
from .serializers import (
    BoardListSerializer,
    BoardDetailSerializer,
    BoardUpdateSerializer,
)
from .permissions import IsMemberOrOwnerOrAdmin


class BoardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing boards.

    Provides CRUD operations for boards with permission handling
    and optimized querysets including aggregated task and member data.
    """

    serializer_class = BoardListSerializer
    permission_classes = [IsAuthenticated, IsMemberOrOwnerOrAdmin]

    def get_queryset(self):
        """
        Return a queryset of boards accessible to the current user.

        Superusers receive all boards. Regular users receive boards
        where they are the owner or a member. The queryset is optimized
        with related data and annotated counts.
        """
        user = self.request.user

        queryset = (
            Board.objects
            .select_related('owner')
            .prefetch_related('members', 'tasks')
            .annotate(
                member_count=Count('members', distinct=True),
                ticket_count=Count('tasks', distinct=True),
                tasks_to_do_count=Count(
                    'tasks',
                    filter=Q(tasks__status='todo'),
                    distinct=True,
                ),
                tasks_high_prio_count=Count(
                    'tasks',
                    filter=Q(tasks__priority='high'),
                    distinct=True,
                ),
            )
        )

        if user.is_superuser:
            return queryset

        return queryset.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

    def create(self, request, *args, **kwargs):
        """
        Create a new board and assign the requesting user as owner.

        Returns the created board with annotated fields included.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        board = serializer.save(owner=request.user)
        board_qs = self.get_queryset().filter(pk=board.pk).first()
        response_serializer = self.get_serializer(board_qs)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def get_object(self):
        """
        Retrieve a board instance by ID and check object permissions.

        Raises:
            NotFound: If the board does not exist.
        """
        board_id = self.kwargs.get("pk")

        try:
            instance = Board.objects.get(pk=board_id)
        except Board.DoesNotExist:
            raise NotFound(detail="Board not found.")

        self.check_object_permissions(self.request, instance)
        return instance

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single board with detailed information.
        """
        instance = self.get_object()
        serializer = BoardDetailSerializer(instance)
        return Response(serializer.data)

    def _update_board(self, request, partial, *args, **kwargs):
        """
        Update a board instance.

        Args:
            partial (bool): Whether the update is partial (PATCH) or full (PUT).
        """
        board = self.get_object()
        serializer = BoardUpdateSerializer(
            board,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a board (PATCH).
        """
        return self._update_board(request, partial=True, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Fully update a board (PUT).
        """
        return self._update_board(request, partial=False, *args, **kwargs)
