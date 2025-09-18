from django.urls import path
from .views import UserListView, UserDetailView, RegistrationView, LoginView

urlpatterns = [
    path('userlist/', UserListView.as_view(), name='user-list'), # List all users
    path('userlist/<int:pk>/', UserDetailView.as_view(), name='user-detail'), # Detail, Update, Delete
    path('registration/', RegistrationView.as_view(), name='registration'),  # You might want to create a separate view for registration
    path('login/', LoginView.as_view(), name='login'),  # You might want to create a separate view for login
]