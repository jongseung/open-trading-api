from .base import BaseStrategy
import time
import pandas as pd

class IntradayTradingStrategy(BaseStrategy):
    """Simple intraday trading using moving average on real-time prices."""

    def __init__(self, api, stock_codes, window=5, interval=60):
        super().__init__(api)
        self.stock_codes = stock_codes
        self.window = window
        self.interval = interval
        self.histories = {code: [] for code in stock_codes}

    def _update_price(self, code):
        info = self.api.get_current_price(code)
        price = int(info.get('stck_prpr', 0))
        hist = self.histories[code]
        hist.append(price)
        if len(hist) > self.window:
            hist.pop(0)
        if len(hist) < self.window:
            return price, None
        return price, sum(hist) / len(hist)

    def _is_holding(self, balance, code):
        if balance.empty or code not in balance.index:
            return False
        qty = int(balance.loc[code]['보유수량'])
        return qty > 0

    def execute(self):
        print(f"Starting intraday trading for: {', '.join(self.stock_codes)}")
        while True:
            balance = self.api.get_acct_balance()
            for code in self.stock_codes:
                price, ma = self._update_price(code)
                if ma is None:
                    continue
                holding = self._is_holding(balance, code)
                if not holding and price > ma:
                    print(f"Buying {code} at {price}")
                    self.api.do_buy(code, 1, price)
                elif holding and price < ma:
                    print(f"Selling {code} at {price}")
                    self.api.do_sell(code, 1, price)
            time.sleep(self.interval)
