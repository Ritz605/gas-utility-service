from rest_framework import generics, permissions
from rest_framework.response import Response

from users.serializers import User, UserSerializer
from .models import ServiceRequest, ServiceRequestFile
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import ServiceRequestFileSerializer, ServiceRequestSerializer, ServiceRequestUpdateSerializer, RequestStatusSerializer
from .permissions import IsCustomerOrReadOnly, IsCustomerOnly
from rest_framework.permissions import IsAuthenticated
from service_requests import serializers

class ServiceRequestCreateView(generics.CreateAPIView):
    """
    Allow customers to create service requests.
    """
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)  # Assign current user as the customer

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class ServiceRequestListView(generics.ListAPIView):
    """
    Customers see their own requests.
    Support reps see all requests.
    """
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read access to all
    filter_backends = [DjangoFilterBackend]  # Enable filtering
    filterset_fields = ['status']  # Allow filtering by status

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return ServiceRequest.objects.all()  # Support reps see all requests
        if user.is_authenticated:
            return ServiceRequest.objects.filter(customer=user)  # Customers see their own
        return ServiceRequest.objects.none()  # Unauthenticated users see nothing

class ServiceRequestDetailView(generics.RetrieveAPIView):
    """
    Retrieve details of a single service request.
    """
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read access to all


class ServiceRequestUpdateView(generics.UpdateAPIView):
    """
    Support reps can update request status.
    """
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        user = self.request.user
        if user.is_staff:  # Only support reps can update status
            serializer.save()
        else:
            raise serializers.ValidationError("You do not have permission to update this request.")

class ServiceRequestDeleteView(generics.DestroyAPIView):
    """
    Customers can delete their own requests.
    """
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOnly]


class RequestStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        service_request = get_object_or_404(ServiceRequest, id=id)
        serializer = RequestStatusSerializer(service_request)
        return Response(serializer.data)

# Update status (only for support reps)
class UpdateRequestStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        service_request = get_object_or_404(ServiceRequest, id=id)

        # Ensure only support reps can update status
        if not request.user.is_staff:
            return Response({"error": "Permission denied. Only support representatives can update status."}, status=403)

        serializer = RequestStatusSerializer(service_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Status updated successfully", "data": serializer.data})
        
        return Response(serializer.errors, status=400)
    

class UploadFileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, id):
        service_request = get_object_or_404(ServiceRequest, id=id)

        if service_request.customer != request.user and not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        file_serializer = ServiceRequestFileSerializer(data={'service_request': service_request.id, 'file': request.FILES['file']})

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListFilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        service_request = get_object_or_404(ServiceRequest, id=id)

        if service_request.customer != request.user and not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        files = ServiceRequestFile.objects.filter(service_request=service_request)
        serializer = ServiceRequestFileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class SupportRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        pending_requests = ServiceRequest.objects.filter(status="Pending")
        serializer = ServiceRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        customers = User.objects.filter(is_staff=False)
        serializer = UserSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        customer = get_object_or_404(User, id=id, is_staff=False)
        serializer = UserSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
