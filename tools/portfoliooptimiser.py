from pandas_datareader import data as web
from pandas.util.testing import assert_frame_equal
import pandas as pd
import numpy as np
import datetime as datetime

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

from pypfopt.efficient_frontier import EfficientFrontier, objective_functions
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices



class Portfolio:
    
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

    def optimise(self, optimisation_technique='max sharpe',risk_free_rate=0.02):
        """
        - Find a way to get the optimised portfolio returns, volatility, discrete allocations etc as class attributes
        - Include arguments into this method to change optimisation parameters such as risk-free-rate, risk-targets etc..
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
        Project possible financial performance using monte carlo
        - Try monte carlo with brownian
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