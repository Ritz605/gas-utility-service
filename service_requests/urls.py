from django.urls import path
from .views import (
    ListFilesView, ServiceRequestListView, ServiceRequestCreateView, ServiceRequestDetailView,
    ServiceRequestUpdateView, ServiceRequestDeleteView,
    RequestStatusView, UpdateRequestStatusView, UploadFileView,
    SupportRequestsView, CustomerListView, CustomerDetailView
)

urlpatterns = [
    path('', ServiceRequestListView.as_view(), name='list_requests'),
    path('new/', ServiceRequestCreateView.as_view(), name='create_request'),
    path('<int:pk>/', ServiceRequestDetailView.as_view(), name='request_detail'),
    path('<int:pk>/update/', ServiceRequestUpdateView.as_view(), name='update_request'),
    path('<int:pk>/delete/', ServiceRequestDeleteView.as_view(), name='delete_request'),

    # Request Tracking APIs
    path('<int:pk>/status/', RequestStatusView.as_view(), name='request-status'),
    path('<int:pk>/status/update/', UpdateRequestStatusView.as_view(), name='update-request-status'),

    path('<int:id>/upload/', UploadFileView.as_view(), name='upload-file'),
    path('<int:id>/files/', ListFilesView.as_view(), name='list-files'),


    
    path('support/requests/', SupportRequestsView.as_view(), name='support-requests'),
    path('customers/', CustomerListView.as_view(), name='list-customers'),
    path('customers/<int:id>/', CustomerDetailView.as_view(), name='customer-detail'),

]
