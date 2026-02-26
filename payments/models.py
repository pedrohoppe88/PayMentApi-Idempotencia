import uuid
from django.db import models


class Payment(models.Model):
    """Model representing a payment with idempotency support."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
        ('refunded', 'Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    idempotency_key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Para retornar o mesmo response HTTP original (nível produção)
    response_body = models.JSONField(null=True, blank=True)
    response_status_code = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment {self.id} - {self.amount} ({self.status})"
