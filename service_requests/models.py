from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="service_requests")
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.customer.username}"


class ServiceRequestFile(models.Model):
    service_request = models.ForeignKey('ServiceRequest', on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='service_request_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)