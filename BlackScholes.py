from numpy import exp, sqrt, log
from scipy.stats import norm


class BlackScholes:
    def __init__(
        self,
        time_to_maturity: float,
        strike: float,
        current_price: float,
        volatility: float,
        interest_rate: float,
    ):
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate

    def run(self):
        T = self.time_to_maturity
        K = self.strike
        S = self.current_price
        σ = self.volatility
        r = self.interest_rate

        # Precompute reusable terms
        sqrtT = sqrt(T)
        vt = σ * sqrtT
        logSK = log(S / K)
        drift = (r + 0.5 * σ ** 2) * T
        d1 = (logSK + drift) / vt
        d2 = d1 - vt
        Nd1 = norm.cdf(d1)
        Nd2 = norm.cdf(d2)
        pdf_d1 = norm.pdf(d1)
        df = exp(-r * T)

        # Option prices
        self.call_price = S * Nd1 - K * df * Nd2
        self.put_price  = K * df * (1 - Nd2) - S * (1 - Nd1)

        # Greeks
        self.call_delta = Nd1
        self.put_delta  = Nd1 - 1
        gamma = pdf_d1 / (S * σ * sqrtT)
        self.call_gamma = gamma
        self.put_gamma  = gamma


if __name__ == "__main__":
    BS = BlackScholes(
        time_to_maturity=2,
        strike=90,
        current_price=100,
        volatility=0.2,
        interest_rate=0.05
    )
    BS.run()
    print(f"Call Price: {BS.call_price:.4f}, Put Price: {BS.put_price:.4f}")
    print(f"Call Delta: {BS.call_delta:.4f}, Put Delta: {BS.put_delta:.4f}")
    print(f"Gamma: {BS.call_gamma:.4f}")
