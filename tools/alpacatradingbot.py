import alpaca_trade_api as tradeapi

secret_key = 'AGsIkmmR8q8DzSSvMj9I0QFIdov23W4ZY6A5v8qn'
api_key_id = 'PKJI5LH5PHGK1P0XZ8IY'

base_url = 'https://paper-api.alpaca.markets'

class AlpacaTradingBot:
    def __init__(self,api_key_id, secret_key, base_url):
        self.api = tradeapi.REST(key_id = api_key_id,
                            secret_key = secret_key,
                            base_url = base_url,
                            api_version = 'v2')
        
    def get_account_info(self, info=[]):
        """
        Inputs list or str:
        id:
        account number:
        status:
        cash:
        portfolio value:
        long market value:
        equity:
        buying power:
        """
        account = self.api.get_account()
        
        if len(info) != 0:
            for i in info:
                if i == 'account number':
                    print(f"Account number: {account.account_number}")
                elif i == 'status':
                    print(f"Account status: {account.status}")
                elif i == 'cash':
                    print(f"Account cash: ${account.cash}")
                elif i == 'portfolio value':
                    print(f"Portfolio value: ${account.portfolio_value}")
                elif i == 'long market value':
                    print(f"Long market value: ${account.long_market_value}")
                elif i == 'equity':
                    print(f"Equity: ${account.equity}")
                elif i == 'buying power':
                    print(f"Buying power: ${account.buying_power}")
                else:
                    print('Make sure that you have entered a valid info metric')
        
        else:
            return account
        
    def get_active_assets(self):
        
        active_assets = self.api.list_assets(status='active')
        
        print(active_assets)
        
    def get_positions(self):
        
        # Get a list of all of our positions.
        positions = self.api.list_positions()

        return positions
    
    def market_open(self):
        
        clock = self.api.get_clock()
        
        if clock.is_open:
            return True
        
        else:
            return False
        
    def place_order(self, ticker, quantity, side):
        """
        Summary: Verifies and then executes orders on Alpaca paper-trading account.
        
        Inputs:
        ticker (str) -- e.g. 'AAPL' 
        quantity (float) -- e.g. 27.0 (must be > 0)
        side (str) -- 'buy' or 'sell'
        """
        #Now that our purchase condition is satisfied we can buy the stock
        order_asset = self.api.get_asset(ticker)
        
        #check that our order is tradable
        if order_asset.tradable:
            self.api.submit_order(
                            symbol=ticker,
                            qty=quantity,
                            side=side,
                            type='market',
                            time_in_force='gtc'
                            )
        else:
            print('Asset is not tradable.')