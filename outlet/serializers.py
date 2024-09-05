from rest_framework import serializers
from .models import Outlet
from auths.serializers import OutletManagerSerializer  # Correct import from the auth app



class OutletSerializer(serializers.ModelSerializer):
    # Use the OutletManagerSerializer to include full manager details
    manager = OutletManagerSerializer(source='manager.userprofile')

    class Meta:
        model = Outlet
        fields = ['id', 'manager', 'outletName', 'location']