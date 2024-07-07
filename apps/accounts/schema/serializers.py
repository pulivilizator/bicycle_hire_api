from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class LoginRegisterResponse200Serializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class LoginRegisterResponse400Serializer(serializers.Serializer):
    error = serializers.CharField()
