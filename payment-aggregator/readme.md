### Payment Aggregator Backend (DRF)

A backend-only, API-first payment aggregator built using Django REST Framework, designed to demonstrate real-world fintech backend concepts: idempotency, async processing, gateway abstraction, webhooks, and state machines.

This project intentionally has no frontend.
Swagger / DRF Browsable API / Postman are the interfaces.

### Project Goals

This project is designed to show how a senior backend engineer thinks, not just writes code.

It demonstrates:

-> Clean DRF architecture
-> Safe payment processing
-> Exactly-once semantics via idempotency
-> Async execution with Celery
-> Gateway abstraction & extensibility
-> Audit-friendly ledger
-> Cloud-ready, Dockerized setup

### System Architecture
Client (Merchant)
   |
   |  REST API (DRF)
   v
Django API Layer
   |
   |-- Authentication (API Key)
   |-- Permissions (Merchant scoped)
   |-- Idempotency
   |
   v
Payment Domain
   |
   |-- State Machine
   |-- Gateway Abstraction
   |
   v
Async Processing (Celery)
   |
   |-- Redis (Broker)
   |-- Retry-safe tasks
   |
   v
Database (Postgres / SQLite)

### Tech Stack

Language: Python 3.11

Framework: Django 4.x, Django REST Framework

Database: PostgreSQL (SQLite for local dev)

Async: Celery + Redis

Infra: Docker, Docker Compose

Auth: API Key (custom DRF authentication)

### Core Features
1 - Payments API

POST /api/payments/ – Create payment

GET /api/payments/{id}/ – Retrieve payment

POST /api/payments/{id}/refund/ – Refund payment

2 - Idempotency

Uses Idempotency-Key header

Guarantees no double charge

Safe for retries and network failures

3 - Async Processing

Payment execution runs in Celery

API returns immediately

Worker handles gateway interaction

4 - Gateway Abstraction

Pluggable gateway interface

Mock success & failure gateways implemented

Easy to add real providers (Stripe, Razorpay, etc.)

5 - Webhooks

Provider → system callback endpoint

Signature verification

Event-level idempotency

State-safe updates

6 - State Machine

Explicit payment lifecycle:

CREATED → PROCESSING → SUCCESS → REFUNDED
                  ↘︎ FAILED


Invalid transitions are blocked.

7 - Immutable Ledger

Every charge/refund writes a ledger entry

No updates, only append

Auditable by design

### Authentication & Security

Custom DRF Authentication

Header: X-API-KEY

Merchant-level isolation

Queryset scoping enforced

No trust in client state

All transitions validated server-side

### DRF Concepts Demonstrated

ModelViewSet

Read vs Write serializers

Custom authentication (BaseAuthentication)

Custom permissions

@action for domain-specific endpoints

Queryset scoping per authenticated entity

APIView for webhooks

Browsable API usage

### Running Locally
1 - Build & Start Services
docker-compose build
docker-compose up

2 -  Run Migrations
docker-compose exec web python manage.py migrate

3 -  Start Celery Worker
docker-compose exec web celery -A config worker -l info

### Example API Usage
Create Payment
curl -X POST http://localhost:8005/api/payments/ \
  -H "X-API-KEY: test_api_key" \
  -H "Idempotency-Key: pay-001" \
  -H "Content-Type: application/json" \
  -d '{"amount": 1000, "currency": "INR"}'

Refund Payment
curl -X POST http://localhost:8005/api/payments/{payment_id}/refund/ \
  -H "X-API-KEY: test_api_key"

### Testing Strategy (Conceptual)

Unit tests for:

-> State machine transitions
-> Idempotency logic
-> Integration tests for:
-> Payment creation
-> Async processing
-> Webhook ingestion
-> Manual testing via DRF Browsable API / curl

### What I’d Add in Production

- Exactly-once delivery guarantees (outbox pattern)
- Circuit breakers per gateway
- Rate limiting per merchant
- Distributed tracing
- Real HMAC webhook signatures
- SQS/Kafka instead of Redis
- Feature flags for gateway routing

### Author Notes

This project is intentionally backend-only.

The focus is:
- correctness
- reliability
- clarity of design
- interview-readiness

It is structured to be easy to reason about and extend, which is critical in fintech systems.