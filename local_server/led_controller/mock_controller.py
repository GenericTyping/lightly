from .led_controller import LedController


class MockController(LedController):
    """A mock controller that does nothing.

    Used for testing and local development."""

    pin: int
    count: int
    order: str

    def __init__(self, pin: int = None, count: int = None, order: str = None):
        self.pin = pin or 18
        self.count = count or 200
        self.order = order or "GRB"
        super().__init__()
