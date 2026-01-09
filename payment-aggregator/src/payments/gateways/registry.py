from .mock_success import MockSuccessGateway
from .mock_failure import MockFailureGateway

GATEWAYS = {
    MockSuccessGateway.name: MockSuccessGateway(),
    MockFailureGateway.name: MockFailureGateway(),
}

def get_gateway(name):
    return GATEWAYS[name]
