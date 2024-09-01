from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    phone_number = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'role', 'phone_number']

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        role = validated_data['role']
        
        # Use phone number as username
        username = phone_number

        # Create User
        user = User.objects.create(username=username)

        # Create UserProfile with the associated User
        UserProfile.objects.create(user=user, role=role, phone_number=phone_number)

        return user
