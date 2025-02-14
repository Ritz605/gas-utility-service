from django.urls import path
from .views import (
    ListFilesView, ServiceRequestListView, ServiceRequestCreateView, ServiceRequestDetailView,
    ServiceRequestUpdateView, ServiceRequestDeleteView,
    RequestStatusView, UpdateRequestStatusView, UploadFileView,
    SupportRequestsView, CustomerListView, CustomerDetailView
)

urlpatterns = [
    path('api/requests/', ServiceRequestListView.as_view(), name='list_requests'),
    path('api/requests/new/', ServiceRequestCreateView.as_view(), name='create_request'),
    path('api/requests/<int:pk>/', ServiceRequestDetailView.as_view(), name='request_detail'),
    path('api/requests/<int:pk>/update/', ServiceRequestUpdateView.as_view(), name='update_request'),
    path('api/requests/<int:pk>/delete/', ServiceRequestDeleteView.as_view(), name='delete_request'),

    # Request Tracking APIs
    path('api/requests/<int:pk>/status/', RequestStatusView.as_view(), name='request-status'),
    path('api/requests/<int:pk>/status/update/', UpdateRequestStatusView.as_view(), name='update-request-status'),

    path('api/requests/<int:id>/upload/', UploadFileView.as_view(), name='upload-file'),
    path('api/requests/<int:id>/files/', ListFilesView.as_view(), name='list-files'),


    
    path('api/support/requests/', SupportRequestsView.as_view(), name='support-requests'),
    path('api/customers/', CustomerListView.as_view(), name='list-customers'),
    path('api/customers/<int:id>/', CustomerDetailView.as_view(), name='customer-detail'),

]
