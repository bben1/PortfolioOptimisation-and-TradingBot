class AlpacaTradingBot:
    """
    Summary:
    Executes trades using the Alpaca API.
    
    Inputs:
    api_key_id -- (str) api_key_id provided by Alpaca when you make an account
    secret_key -- (str) secret_key provided by Alpaca when you make an account
    base_url -- (str) refer to Alpaca API documentation
    """
    def __init__(self,api_key_id, secret_key, base_url):
        self.api = tradeapi.REST(key_id = api_key_id,
                            secret_key = secret_key,
                            base_url = base_url,
                            api_version = 'v2')
        
    def get_account_info(self, info=[]):
        """
        Summary:
        get Alpaca account information
        
        Inputs:
        info -- (list/str) any of ['id','account number','status','cash','portfolio value','long market value','equity','buying power']
        
        Returns:
        account information
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
        """
        Summary:
        get list of active assets
        
        Returns:
        (json) active assets
        """
        active_assets = self.api.list_assets(status='active')
        
        return active_assets
        
    def get_positions(self):
        """
        Summary:
        get list of portfolio positions
        
        Returns:
        (json) portfolio positions
        """
        # Get a list of all of our positions.
        positions = self.api.list_positions()

        return positions
    
    def market_open(self):
        """
        Summary:
        find out if the market is open
        
        Returns:
        (bool)
        """
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
        
        Returns:
        (json) summary of transaction
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
            
