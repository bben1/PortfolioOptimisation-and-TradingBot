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

from tools.portfoliooptimiser import Portfolio
from tools.alpacatradingbot import AlpacaTradingBot

base_url = 'https://paper-api.alpaca.markets'
