from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "password", "email", "is_staff")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        password = validated_data.pop("password")
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
