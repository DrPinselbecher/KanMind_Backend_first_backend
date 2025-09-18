# 2. Third-party
from django.contrib.auth.models import User
from rest_framework import serializers



class UserProfileSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source="username")

    class Meta:
        model = User
        fields = ["fullname", "email", "id"]

    def validate_fullname(self, value):
        if User.objects.filter(username__iexact=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Username already taken.")
        return value
    

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, trim_whitespace=False)
    repeat_password = serializers.CharField(write_only=True, trim_whitespace=False)
    fullname = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = ["fullname", "email", "password", "repeat_password"]

    def validate(self, attrs):
        if attrs["password"] != attrs["repeat_password"]:
            raise serializers.ValidationError({"repeat_password": "Passwords must match."})
        return attrs

    def validate_fullname(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def create(self, validated_data):
        validated_data.pop("repeat_password")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user