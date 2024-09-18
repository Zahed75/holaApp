from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='userprofile.phone_number', read_only=True)
    role = serializers.CharField(source='userprofile.role', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'role', 'phone_number','role','username']

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
        fields = ['phone_number', 'first_name', 'last_name', 'email']

    def to_representation(self, instance):
        """Override to_representation to include the user's details."""
        representation = super().to_representation(instance)
        # Add the user-related fields
        representation['first_name'] = instance.user.first_name
        representation['last_name'] = instance.user.last_name
        representation['email'] = instance.user.email
        return representation