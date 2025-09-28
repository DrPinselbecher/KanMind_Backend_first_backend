# third party imports
from django.db.models import Count, Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import IsMemberOrOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated, PermissionDenied, NotFound
from django.shortcuts import get_object_or_404


# local imports
from boards_app.models import Board
from .serializers import BoardListSerializer, BoardDetailSerializer



class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardListSerializer
    permission_classes = [IsAuthenticated, IsMemberOrOwnerOrAdmin]

    def get_queryset(self):
        return (
            Board.objects
            .filter(Q(owner=self.request.user) | Q(members=self.request.user)).distinct()
            .select_related('owner')
            .prefetch_related('members', 'tasks')
            .annotate(
                member_count=Count('members', distinct=True),
                ticket_count=Count('tasks', distinct=True),
                tasks_to_do_count=Count('tasks', filter=Q(tasks__status='todo'), distinct=True),
                tasks_high_prio_count=Count('tasks', filter=Q(tasks__priority='high'), distinct=True),
            )
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = serializer.save(owner=request.user)
        board_qs = self.get_queryset().filter(pk=board.pk).first()
        response_serializer = self.get_serializer(board_qs)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def get_object(self):
        board_id = self.kwargs.get("pk")
        try:
            instance = Board.objects.get(pk=board_id)
        except Board.DoesNotExist:
            raise NotFound(detail="Board not found.")
        self.check_object_permissions(self.request, instance)
        return instance

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BoardDetailSerializer(instance)
        return Response(serializer.data)