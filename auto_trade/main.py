from auto_trade.config import load_env, apply_to_kis_api
import rest.kis_api as kis_api
from auto_trade.strategies.simple import MovingAverageStrategy


def main():
    env = load_env()
    apply_to_kis_api(env)

    svr = env.get('svr', 'vps')
    product = env.get('product', '01')
    stock_code = env.get('stock_code', '005930')

    kis_api.auth(svr=svr, product=product)

    strategy = MovingAverageStrategy(kis_api, stock_code)
    strategy.execute()


if __name__ == "__main__":
    main()
