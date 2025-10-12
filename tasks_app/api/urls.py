from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TasksViewSet, TaskAssignedToCurrentUser, TaskreviewingCurrentUser

router = DefaultRouter()
router.register(r'', TasksViewSet, basename='tasks')

urlpatterns = [
    path('assigned-to-me/', TaskAssignedToCurrentUser.as_view(), name='tasks-assigned-to-me'),
    path('reviewing/', TaskreviewingCurrentUser.as_view(), name='tasks-reviewing'),
    path('', include(router.urls)),
]
