class Portfolio:
    """
    Summary:
    Creates portfolio of companies in the stock market.
    
    Inputs:
    assets -- (list/str) list of tickers of the companies that are going to be in the portfolio.
    weights -- (list/float) list of weights associated with the portfolio companies.
    start_balance -- (float) opening balance of the portfolio (budget).
    start_date -- (date) start-date from which historical analysis will begin)
    end_date -- (date) date from which historical analysis ends.
    
    returns:
    Plot of adj closing prices of the assets between the start and end dates.
    
    """
    def __init__(self, assets, weights, start_balance, start_date, end_date):
        
        self.assets = assets
        self.weights = weights
        self.start_balance = start_balance
        self.start_date = start_date
        self.end_date = end_date
        
        self.adj_close_prices = pd.DataFrame()
        
        self.create_df(plot=True)
        
        self.daily_returns = self.adj_close_prices.pct_change()
        
    def create_df(self, plot = False):
        """
        Summary: 
        Creates a dataframe of the adj. close prices of each asset within the start and end dates.
        
        Inputs:
        plot -- (bool) if True, plots the adj. close prices.
        
        """
        for stock in self.assets:
            self.adj_close_prices[stock] = web.DataReader(stock,
                                                          data_source='yahoo',
                                                          start = self.start_date,
                                                          end = self.end_date)['Adj Close']
        
        if plot:
        #Visually show the stock portfolio
            title = f'Adj Close asset prices'
            #create and plot the graph
            for c in self.adj_close_prices.columns.values:
                plt.plot(self.adj_close_prices[c], label = c, linewidth = 0.5)

            plt.title(title)
            plt.xlabel('date', fontsize=18)
            plt.ylabel('Adj Close ($)', fontsize=18)
            plt.legend(self.adj_close_prices.columns.values, loc='upper left')
            plt.show()

    def optimise(self, optimisation_technique = 'max sharpe', risk_free_rate = 0.02):
        """
        Summary: 
        Calculates optimal portfolio allocation to satisfy portfolio objectives.
        
        Inputs:
        optimisation_technique -- (str) 'max sharpe' or 'min volatilty'.
        risk_free_rate -- (float) estimate of the risk-free-rate.
        
        Returns:
        Portfolio forecast summary -- Expected return, Expected volatility, Expected Sharpe Ratio
        
        Prints:
        Discrete share allocation
        Liquid funds remaining
        
        """
        #Calculate the expected returns and the annualised sample covariance matrix of asset returns
        self.annual_return = expected_returns.mean_historical_return(self.adj_close_prices)
        self.cov = risk_models.sample_cov(self.adj_close_prices)

        #Optimize max sharpe ratio
        ef = EfficientFrontier(self.annual_return, self.cov)
        
        if optimisation_technique == 'max sharpe':
            self.weights = ef.max_sharpe(risk_free_rate = risk_free_rate)
        elif optimisation_technique == 'min volatility':
            self.weights = ef.min_volatility()
        else:
            print("Enter one of the following: ['max sharpe','min volatility']")
        
        self.weights = ef.clean_weights()
        
        #Discrete allocation to find the optimal purchase of each security using the latest prices
        self.latest_prices = get_latest_prices(self.adj_close_prices)
        da = DiscreteAllocation(weights = self.weights,
                                latest_prices = self.latest_prices,
                                total_portfolio_value = self.start_balance)
        
        #Print results after optimization
        print("*****************************************************************")
        self.summary = ef.portfolio_performance(verbose=True)
        print("*****************************************************************")
        
        self.allocation, self.balance = da.lp_portfolio()
        self.annual_return = self.summary[0]
        self.vol = self.summary[1]
        self.sharpe_ratio = self.summary[2]
        self.portfolio_value = self.start_balance-self.balance
        
        print(f'Discrete share allocation: {self.allocation}')
        print('Liquid funds remaining: $' + "{:.2f}".format(self.balance))
        print("*****************************************************************")
        
    def monte_carlo(self, time_horizon=5, annual_addition=0, iterations=300, plot=False):
        """
        Summary:
        Projects the value of the portfolio after a time-horizon using Monte Carlo Simulation.
        
        Inputs:
        time_horizon -- (int) The length of time (years) before you exit all portfolio positions.
        annual_addition -- (float) The amount of money that will be consistently added to the portfolio on an annual basis.
        iterations -- (int) The number of iterations to perform the monte carlo simulation.
        plot -- (bool) If true, returns a plot showing the distribution of projected portfolio value.
        
        Returns:
        Summary of the monte carlo simulation with key statistics.
        If plot, returns a plot showing the distribution of projected portfolio value.
        
        """
        sim = pd.DataFrame()
        
        for x in range(iterations):

            fv = self.portfolio_value
            stream = [fv]
            
            for year in range(time_horizon):
                
                market_return = np.random.normal(self.annual_return, self.vol)
                fv = fv*(1+market_return) + annual_addition
                end = round(fv,2)

                stream.append(end)
                year += 1

            sim[x] = stream
           
        prices = sim.iloc[-1]
        
        print("Summary of Monte Carlo simulation:\n")
        print(f"Time horizon: {time_horizon} years\nConstant annual investment: ${annual_addition}\n")
        print(prices.describe())
        print("*****************************************************************")
        
        if plot:
            
            plt.hist(prices,bins=50,histtype='bar',label='label',color='green',density=True,alpha=0.4)
            plt.xlabel('Projected portfolio returns')
            plt.ylabel('Probability')
            plt.title(f'Monte carlo simulation at {iterations} iterations.')
            
         
