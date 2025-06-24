class BaseStrategy:
    """Base class for trading strategies."""

    def __init__(self, api):
        self.api = api

    def execute(self):
        """Run trading logic."""
        raise NotImplementedError("Strategy must implement execute method")
