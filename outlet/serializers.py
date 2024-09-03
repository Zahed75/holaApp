from rest_framework import serializers
from .models import Outlet

class OutletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outlet
        fields = ['id', 'manager', 'outletName', 'location']

    def create(self, validated_data):
        return Outlet.objects.create(**validated_data)
