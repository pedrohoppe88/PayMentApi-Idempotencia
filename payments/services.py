from decimal import Decimal
from .repositories import PaymentRepository
from .models import Payment


class PaymentGatewayInterface:
    """Interface para gateway de pagamento (Dependency Inversion Principle)."""
    
    def charge(self, amount: Decimal) -> dict:
        """Método para processar pagamento. Debe ser implementado pelas subclasses."""
        raise NotImplementedError


class FakePaymentGateway(PaymentGatewayInterface):
    """Simulação de gateway de pagamento."""
    
    def charge(self, amount: Decimal) -> dict:
        """
        Simula processamento de pagamento.
        Em produção, isso seria uma chamada real ao gateway (Stripe, Mercado Pago, etc.)
        """
        # Simula processamento bem-sucedido
        return {
            'status': 'approved',
            'gateway_transaction_id': f'txn_{id(amount)}'
        }


class PaymentService:
    """Service layer contendo a lógica de negócio de pagamentos."""
    
    def __init__(self, gateway: PaymentGatewayInterface = None):
        self.gateway = gateway or FakePaymentGateway()
    
    def process_payment(self, amount: Decimal, idempotency_key: str) -> tuple:
        """
        Processa um pagamento com suporte a idempotência.
        
        Returns:
            tuple: (payment, created) - payment object and boolean indicating if it was created
        """
        # 1. Verifica se já existe pagamento com esta chave de idempotência
        existing_payment = PaymentRepository.get_by_idempotency_key(idempotency_key)
        
        if existing_payment:
            return existing_payment, False  # Já existia, não cria novamente
        
        # 2. Processa o pagamento via gateway
        gateway_response = self.gateway.charge(amount)
        
        # 3. Cria o pagamento no banco de dados
        payment = PaymentRepository.create(
            amount=amount,
            status=gateway_response['status'],
            idempotency_key=idempotency_key,
            response_body=gateway_response,
            response_status_code=200
        )
        
        return payment, True
    
    def get_payment(self, payment_id: str) -> Payment:
        """Retorna um pagamento pelo ID."""
        return PaymentRepository.get_by_id(payment_id)
