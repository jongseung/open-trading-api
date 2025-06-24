from auto_trade.config import load_env, apply_to_kis_api
import rest.kis_api as kis_api
from auto_trade.strategies.simple import MovingAverageStrategy
from auto_trade.strategies.intraday import IntradayTradingStrategy


def main():
    env = load_env()
    apply_to_kis_api(env)

    svr = env.get('svr', 'vps')
    product = env.get('product', '01')
    strategy_name = env.get('strategy', 'simple')

    kis_api.auth(svr=svr, product=product)

    if strategy_name == 'intraday':
        codes = env.get('stock_codes', env.get('stock_code', '005930')).split(',')
        codes = [c.strip() for c in codes if c.strip()]
        strategy = IntradayTradingStrategy(kis_api, codes)
    else:
        stock_code = env.get('stock_code', '005930')
        strategy = MovingAverageStrategy(kis_api, stock_code)

    strategy.execute()


if __name__ == "__main__":
    main()
