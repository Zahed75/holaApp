from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile



# class UserSerializer(serializers.ModelSerializer):
#     # Fetch phone_number and role from the related UserProfile model
#     phone_number = serializers.SerializerMethodField()
#     role = serializers.SerializerMethodField()
#     manager_id = serializers.SerializerMethodField()  # Changed from unique_user_id to manager_id
#
#     class Meta:
#         model = User
#         fields = ['id', 'first_name', 'last_name', 'email', 'username', 'phone_number', 'role', 'manager_id']
#
#     def get_phone_number(self, obj):
#         # Get the phone_number from the related UserProfile
#         try:
#             return obj.userprofile.phone_number
#         except UserProfile.DoesNotExist:
#             return None
#
#     def get_role(self, obj):
#         # Get the role from the related UserProfile
#         try:
#             return obj.userprofile.role
#         except UserProfile.DoesNotExist:
#             return None
#
#     def get_manager_id(self, obj):
#         # Get the unique_user_id from the related UserProfile, but call it manager_id in the response
#         try:
#             return obj.userprofile.unique_user_id
#         except UserProfile.DoesNotExist:
#             return None
#
#






class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    manager_id = serializers.SerializerMethodField()  # Alias for unique_user_id

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'phone_number', 'role', 'manager_id']

    def get_phone_number(self, obj):
        try:
            return obj.userprofile.phone_number
        except UserProfile.DoesNotExist:
            return None

    def get_role(self, obj):
        try:
            return obj.userprofile.role
        except UserProfile.DoesNotExist:
            return None

    def get_manager_id(self, obj):
        try:
            return obj.userprofile.unique_user_id
        except UserProfile.DoesNotExist:
            return None




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

