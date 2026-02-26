# PayMentAPI - API de Pagamentos com Suporte a Idempotência

<p align="center">
  <img src="https://img.shields.io/badge/Django-6.0.2-green" alt="Django">
  <img src="https://img.shields.io/badge/DRF-REST%20Framework-blue" alt="DRF">
  <img src="https://img.shields.io/badge/Python-3.14-yellow" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-orange" alt="License">
</p>

## 📚 O que é Idempotência?

### Definição Técnica

**Idempotência** é uma propriedade fundamental em APIs e sistemas distribuídos que garante que uma operação pode ser aplicada múltiplas vezes sem alterar o resultado além da primeira aplicação.

> Em termos simples: fazer a mesma solicitação várias vezes deve produzir o mesmo resultado que fazê-la apenas uma vez.

### Por que Idempotência é Crítica em Pagamentos?

Em sistemas de pagamento, falhas de rede, timeouts ou erros de cliente podem fazer com que o usuário tente enviar a mesma requisição várias vezes. Sem idempotência:

```
Usuário clica "Pagar" 3 vezes
    ↓
3 requisições são enviadas ao servidor
    ↓
Sem idempotência: 3 cobranças são feitas no cartão! 💸💸💸
Com idempotência: apenas 1 cobrança é realizada ✅
```

---

## 🔑 O que é Idempotency-Key?

### Conceito

A **Idempotency-Key** (chave de idempotência) é um identificador único que o cliente envia junto com a requisição para garantir que a operação seja executada apenas uma vez.

### Como Funciona

1. **Cliente gera uma chave única** (UUID, hash ou qualquer identificador único)
2. **Cliente envia a requisição** incluindo a `Idempotency-Key` no header
3. **Servidor verifica** se já existe uma operação com essa chave
4. **Se já existe**: retorna o resultado da operação original (sem reprocessar)
5. **Se não existe**: processa a operação e armazena o resultado com a chave

### Exemplo de Uso

```http
POST /api/payments/ HTTP/1.1
Host: 127.0.0.1:8000
Idempotency-Key: order-12345-abcde
Content-Type: application/json

{
  "amount": 150.00
}
```

**Resposta (primeira vez - created: true):**
```
json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "amount": "150.00",
  "status": "approved",
  "created": true,
  "idempotency_key": "order-12345-abcde"
}
```

**Resposta (segunda vez com mesma chave - created: false):**
```
json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "amount": "150.00",
  "status": "approved",
  "created": false,
  "idempotency_key": "order-12345-abcde"
}
```

---

## 🏗️ Arquitetura do Projeto

Este projeto segue os princípios **SOLID** e utiliza uma arquitetura em camadas:

```
┌─────────────────────────────────────────────────────────────┐
│                      Views (API)                            │
│                  payments/views.py                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    Services                                  │
│               payments/services.py                          │
│  - PaymentService: lógica de negócio                        │
│  - FakePaymentGateway: simulação do gateway                 │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   Repositories                               │
│              payments/repositories.py                       │
│  - operações de banco de dados                              │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      Models                                  │
│               payments/models.py                            │
│  - Payment: modelo do pagamento                              │
└─────────────────────────────────────────────────────────────┘
```

### Componentes

| Componente | Arquivo | Responsabilidade |
|------------|---------|------------------|
| **Model** | `payments/models.py` | Define a estrutura do banco de dados (Payment) |
| **Repository** | `payments/repositories.py` | Abstração do acesso a dados |
| **Service** | `payments/services.py` | Lógica de negócio e idempotência |
| **Serializer** | `payments/serializers.py` | Validação e serialização JSON |
| **View** | `payments/views.py` | Endpoints da API REST |

---

## 📦 Modelo de Dados

### Payment

```
python
class Payment(models.Model):
    id = models.UUIDField(primary_key=True)          # UUID único
    amount = models.DecimalField(...)                 # Valor do pagamento
    status = models.CharField(...)                    # pending, approved, refused, refunded
    idempotency_key = models.CharField(unique=True)  # Chave de idempotência
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    response_body = models.JSONField(...)            # Resposta original do gateway
    response_status_code = models.IntegerField(...)  # Status HTTP original
```

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.14+
- Django 6.0.2
- Django REST Framework

### Instalação

1. **Clone o repositório:**
```
bash
cd PayMentAPI
```

2. **Crie um ambiente virtual (opcional mas recomendado):**
```
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências:**
```
bash
pip install django djangorestframework
```

4. **Execute as migrações:**
```
bash
python manage.py migrate
```

5. **Inicie o servidor:**
```
bash
python manage.py runserver
```

6. **Acesse a API:**
```
http://127.0.0.1:8000/api/
```

---

## 📡 Endpoints da API

### POST /api/payments/

Cria um novo pagamento com suporte a idempotência.

**Headers:**
| Header | Obrigatório | Descrição |
|--------|-------------|------------|
| `Idempotency-Key` | ✅ | Chave única para idempotência |

**Body:**
```
json
{
  "amount": 150.00
}
```

**Resposta (201 Created):**
```
json
{
  "id": "uuid-aqui",
  "amount": "150.00",
  "status": "approved",
  "created": true,
  "idempotency_key": "sua-chave-aqui"
}
```

---

## 💡 Exemplos Práticos

### Usando cURL

```
bash
# Primeira requisição (cria o pagamento)
curl -X POST http://127.0.0.1:8000/api/payments/ \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: pedido-001" \
  -d '{"amount": 199.90}'

# Segunda requisição com mesma chave (retorna pagamento existente)
curl -X POST http://127.0.0.1:8000/api/payments/ \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: pedido-001" \
  -d '{"amount": 199.90}'
```

### Usando Python

```
python
import requests

url = "http://127.0.0.1:8000/api/payments/"
headers = {
    "Content-Type": "application/json",
    "Idempotency-Key": "order-12345"
}
data = {"amount": 250.00}

# Primeira requisição
response1 = requests.post(url, json=data, headers=headers)
print(response1.json())
# {'created': True, 'status': 'approved', ...}

# Segunda requisição (mesma chave)
response2 = requests.post(url, json=data, headers=headers)
print(response2.json())
# {'created': False, 'status': 'approved', ...}
```

---

## 🔒 Boas Práticas de Idempotência

### 1. Gere chaves únicas no cliente
```
python
import uuid
idempotency_key = str(uuid.uuid4())
# ou
idempotency_key = f"order-{order_id}-{timestamp}"
```

### 2. Use o mesmo header padrão
A maioria das APIs usa `Idempotency-Key` (com K maiúsculo e hífen).

### 3. A chave deve ser única por operação
- Para cada **cliente + 请求** diferente, use uma chave diferente
- A chave deve ter vida útil razoável (geralmente 24-72 horas)

### 4. Sempre use HTTPS
Para garantir que a chave não seja interceptada.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| **Django** | 6.0.2 | Framework web Python |
| **Django REST Framework** | - | Framework para APIs REST |
| **SQLite** | - | Banco de dados (desenvolvimento) |
| **Python** | 3.14+ | Linguagem de programação |


## 🎯 Conclusão

Este projeto demonstra:

- ✅ **Conceito de Idempotência** - Essencial para sistemas de pagamento
- ✅ **Arquitetura RESTful** - Boas práticas de API
- ✅ **Padrões de Projeto** - SOLID, Repository Pattern, Service Layer
- ✅ **Validação de Dados** - Serializers do DRF
- ✅ **UUID** - Identificadores únicos seguros
- ✅ **Tratamento de Erros** - Responses consistentes
