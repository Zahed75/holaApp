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



class OutletManagerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ['phone_number','first_name', 'last_name', 'email']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['email'],  # assuming email is used as the username
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email']
        )
        user_profile = UserProfile.objects.create(user=user, role='outlet_manager', **validated_data)
        return user_profile
