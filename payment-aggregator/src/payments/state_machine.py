class PaymentStates:
    CREATED = "CREATED"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


ALLOWED_TRANSITIONS = {
    PaymentStates.CREATED: [PaymentStates.PROCESSING],
    PaymentStates.PROCESSING: [PaymentStates.SUCCESS, PaymentStates.FAILED],
    PaymentStates.SUCCESS: [PaymentStates.REFUNDED],
}


def can_transition(from_state, to_state):
    return to_state in ALLOWED_TRANSITIONS.get(from_state, [])
