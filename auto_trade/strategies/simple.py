from .base import BaseStrategy


class MovingAverageStrategy(BaseStrategy):
    """Very simple moving average based strategy."""

    def __init__(self, api, stock_code: str, window: int = 5):
        super().__init__(api)
        self.stock_code = stock_code
        self.window = window

    def execute(self):
        history = self.api.get_stock_history_by_ohlcv(self.stock_code)
        if history.empty:
            print("No price history available")
            return

        close = history['Close']
        ma = close.rolling(self.window).mean().iloc[-1]
        price = close.iloc[-1]

        balance = self.api.get_acct_balance()
        holding = False
        if not balance.empty and self.stock_code in balance.index:
            qty = int(balance.loc[self.stock_code]['보유수량'])
            holding = qty > 0
        if not holding and price > ma:
            print(f"Buying {self.stock_code} at {price}")
            self.api.do_buy(self.stock_code, 1, price)
        elif holding and price < ma:
            print(f"Selling {self.stock_code} at {price}")
            self.api.do_sell(self.stock_code, 1, price)
