from rest_framework import serializers
from .models import ServiceRequest, ServiceRequestFile, User

class ServiceRequestSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.username')  # Only read customer username

    class Meta:
        model = ServiceRequest
        fields = ['id', 'customer', 'title', 'description', 'status', 'created_at']
        read_only_fields = ['customer', 'status', 'created_at']  # Status updated by support reps

class ServiceRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['status']

class RequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['status']


class ServiceRequestFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequestFile
        fields = ['id', 'service_request', 'file', 'uploaded_at']


class ServiceRequestSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.username')  # Customer is read-only, sourced from the username

    class Meta:
        model = ServiceRequest
        fields = ['id', 'customer', 'title', 'description', 'status', 'created_at']
        read_only_fields = ['customer', 'status', 'created_at']  # Ensure these are not expected in the payload


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']