# third party imports
from django.db.models import Count, Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import IsBoardMemberOrOwner


# local imports
from boards_app.models import Board
from .serializers import BoardSerializer



class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [IsBoardMemberOrOwner]

    def get_queryset(self):
        return (
            Board.objects
            .filter(owner=self.request.user)
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