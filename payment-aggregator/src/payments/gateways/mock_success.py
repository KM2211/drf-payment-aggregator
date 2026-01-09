from .base import BaseGateway

class MockSuccessGateway(BaseGateway):
    name = "mock_success"

    def charge(self, payment):
        return {
            "status": "SUCCESS",
            "gateway_reference": f"success-{payment.id}"
        }
