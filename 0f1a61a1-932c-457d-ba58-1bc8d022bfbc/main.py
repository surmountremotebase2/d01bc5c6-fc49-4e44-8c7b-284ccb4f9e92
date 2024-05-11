from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, InstitutionalOwnership, InsiderTrading, FundamentalData
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"] # Example tickers known for being "wonderful businesses"
        self.data_list = [FundamentalData(i) for i in self.tickers]

    @property
    def interval(self):
        return "1week" # Longer intervals may better suit the buy-and-hold with fundamental analysis

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def is_undervalued(self, asset_data):
        """
        Simplified method to check if an asset may be considered undervalued.
        Here we use P/E ratio lower than a threshold as a proxy; in a real-case scenario,
        a more in-depth analysis would be necessary.
        """
        pe_ratio = asset_data.get('pe_ratio', float('inf')) # Example access, assuming a P/E ratio is available
        institutional_ownership = asset_data.get('institutional_ownership', 0)
        insider_sales = asset_data.get('insider_sales', 0)
        # A very basic and theoretical filter to define undervalued:
        # P/E ratio is under a threshold, and institutional ownership is high indicating solid investor trust
        return pe_ratio < 20 and institutional_ownership > 50 and insider_sales == 0

    def run(self, data):
        allocation_dict = {}
        for ticker, asset_data in data.items():
            if self.is_undervalued(asset_data):
                allocation_dict[ticker] = 1.0 / len([t for t in self.tickers if self.is_undervalued(data[t])]) # Evenly distribute amongst undervalued assets
            else:
                allocation_dict[ticker] = 0 # Do not allocate to overvalued assets

        return TargetAllocation(allocation_dict)