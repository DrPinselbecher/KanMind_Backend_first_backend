from django.urls import path, include
from .views import RegistrationView, LoginView, UserViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)), # List and detail views for UserViewSet

    path('registration/', RegistrationView.as_view(), name='registration'),  # You might want to create a separate view for registration
    path('login/', LoginView.as_view(), name='login'),  # You might want to create a separate view for login
]