from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    phone_number = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'role', 'phone_number']

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        username = phone_number  # Use phone number as username since email is not used

        user = User.objects.create(
            username=username
        )
        return user
