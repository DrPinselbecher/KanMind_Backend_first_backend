from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view



@api_view(["GET"])
def check_email(request):
    email = request.query_params.get("email")

    if not email:
        return Response({"detail": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    if "@" not in email or "." not in email:
        return Response({"detail": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(User, email=email)
    return Response(
        {
            "id": user.id,
            "email": user.email,
            "fullname": f"{user.first_name} {user.last_name}".strip()
        },
        status=status.HTTP_200_OK
    )
