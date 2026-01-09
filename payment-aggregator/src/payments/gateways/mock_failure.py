from .base import BaseGateway

class MockFailureGateway(BaseGateway):
    name = "mock_failure"

    def charge(self, payment):
        return {
            "status": "FAILED",
            "gateway_reference": f"failed-{payment.id}"
        }
