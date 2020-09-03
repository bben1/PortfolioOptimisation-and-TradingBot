import pandas as pd
import numpy as np
import datetime as datetime
from pandas_datareader import data as web
from pandas.util.testing import assert_frame_equal

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

from pypfopt.efficient_frontier import EfficientFrontier, objective_functions
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

import alpaca_trade_api as tradeapi

from tools.portfoliooptimiser import Portfolio
from tools.alpacatradingbot import AlpacaTradingBot

def main(secret_api, api_key_id, base_url):
    #stocks that we will be investing in
    tech = ['FB','AMZN','AAPL','NFLX','GOOG','TSLA','SNAP']

    #finding the optimal portfolio allocation
    weight = 1/len(tech)
    weights = [weight for i in range(len(tech))]
    start = datetime.date(2013,1,1)
    end = datetime.date(2020,8,23)

    portfolio = Portfolio(assets = tech, weights = weights, start_balance = 100000, start_date = start, end_date = end)
    portfolio.optimise('max sharpe')
    portfolio.monte_carlo(time_horizon = 15, annual_addition = 10000, iterations = 5000, plot = True)
  
    #instantiate the api
    base_url = 'https://paper-api.alpaca.markets'
    
    bot = AlpacaTradingBot(api_key_id = api_key_id,
                           secret_key = secret_api,
                           base_url = base_url)
    
    for i in tech:
        try:
            bot.place_order(ticker=i,
                            quantity = portfolio.allocation[i],
                            side='buy')
        except KeyError:
            pass
        #add exception that catches lack of funds.
    
    #View a summary of our portfolio
    return bot.get_positions()

if __name__ == '__main__':
    secret_api = #Your secret API key
    api_key_id = #Your API key id
    base_url = 'https://paper-api.alpaca.markets'
    main(secret_api = secret_api, api_key_id=api_key_id, base_url=base_url)
