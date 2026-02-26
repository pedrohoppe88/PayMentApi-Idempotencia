from .models import Payment


class PaymentRepository:
    
    @staticmethod
    def get_by_idempotency_key(key: str):
        return Payment.objects.filter(idempotency_key=key).first()
    
    @staticmethod
    def get_by_id(payment_id: str):
        return Payment.objects.filter(id=payment_id).first()
    
    @staticmethod
    def create(**kwargs):
        return Payment.objects.create(**kwargs)
    
    @staticmethod
    def update(payment, **kwargs):
        for key, value in kwargs.items():
            setattr(payment, key, value)
        payment.save()
        return payment

    