from abc import ABC, abstractmethod

class BaseGateway(ABC):
    name = None

    @abstractmethod
    def charge(self, payment):
        """
        Simulate charging a payment.
        Must return a dict with status and reference.
        """
        pass
