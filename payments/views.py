from urllib import request

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import PaymentService
from .serializers import PaymentSerializer, PaymentResponseSerializer


class PaymentView(APIView):
    """
    API View para processar pagamentos.
    
    Endpoint: POST /api/payments/
    
    Headers required:
        - Idempotency-Key: chave única para evitar duplicação
    
    Body:
        {
            "amount": 100.00
        }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payment_service = PaymentService()
    
    def post(self, request):
        # 1. Valida os dados da requisição
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 2. Verifica se a chave de idempotência foi enviada
        idempotency_key = request.headers.get('Idempotency-Key')
        
        if not idempotency_key:
            return Response(
                {'error': 'Idempotency-Key header is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 3. Processa o pagamento
        payment, created = self.payment_service.process_payment(
            amount=serializer.validated_data['amount'],
            idempotency_key=idempotency_key
        )
        
        # 4. Retorna a resposta
        response_serializer = PaymentResponseSerializer(payment)
        
        return Response({
            'id': str(payment.id),
            'amount': str(payment.amount),
            'status': payment.status,
            'created': created,
            'idempotency_key': payment.idempotency_key
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class PaymentDetailView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payment_service = PaymentService()

    def post(self, request):

        # 👇 ADICIONE AQUI
        idempotency_key = request.headers.get('Idempotency-Key')
        print("IDEMPOTENCY RECEBIDA:", idempotency_key)

        # valida serializer
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not idempotency_key:
            return Response(
                {'error': 'Idempotency-Key header is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment, created = self.payment_service.process_payment(
            amount=serializer.validated_data['amount'],
            idempotency_key=idempotency_key
        )

        return Response({
            'id': str(payment.id),
            'amount': str(payment.amount),
            'status': payment.status,
            'created': created,
            'idempotency_key': payment.idempotency_key
        })
        
        


    