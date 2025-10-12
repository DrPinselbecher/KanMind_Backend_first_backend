from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TasksViewSet, TaskAssignedToCurrentUser, TaskReviewingCurrentUser, TaskCommentsViewSet

router = DefaultRouter()
router.register('', TasksViewSet, basename='tasks')

urlpatterns = [
    path('<int:task_pk>/comments/', TaskCommentsViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='task-comments-list'),

    path('<int:task_pk>/comments/<int:pk>/', TaskCommentsViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
    }), name='task-comments-detail'),

    path('assigned-to-me/', TaskAssignedToCurrentUser.as_view(), name='tasks-assigned-to-me'),
    path('reviewing/', TaskReviewingCurrentUser.as_view(), name='tasks-reviewing'),
    path('', include(router.urls)),
]
