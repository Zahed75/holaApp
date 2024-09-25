from rest_framework import serializers
from .models import Outlet
from django.contrib.auth.models import User  # Import User model
from auths.models import *






class OutletSerializer(serializers.ModelSerializer):
    # Accept manager's unique_user_id in the request
    manager = serializers.CharField(write_only=True)
    manager_details = serializers.SerializerMethodField(read_only=True)  # Manager details

    class Meta:
        model = Outlet
        fields = ['id', 'manager', 'manager_details', 'outletName', 'location']

    def get_manager_details(self, obj):
        # Return the manager's details in the response
        manager_profile = UserProfile.objects.get(user=obj.manager)
        return {
            'id': manager_profile.unique_user_id,
            'first_name': obj.manager.first_name,
            'last_name': obj.manager.last_name,
            'email': obj.manager.email,
            'phone_number': manager_profile.phone_number,
            'role': manager_profile.role
        }

    def create(self, validated_data):
        # Extract the manager's unique_user_id from the data
        manager_unique_id = validated_data.pop('manager')

        # Find the manager's UserProfile using the unique ID
        try:
            user_profile = UserProfile.objects.get(unique_user_id=manager_unique_id)
            manager_user = user_profile.user  # Get the related User object
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError('Manager with this unique ID does not exist.')

        # Create the outlet and associate it with the found manager
        outlet = Outlet.objects.create(manager=manager_user, **validated_data)
        return outlet
