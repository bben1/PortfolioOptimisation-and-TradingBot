# PortfolioOptimisationTradingBot

#### This project is for educational purposes and should not be used as a guide for financial decisions.

## Project summary:
A tool that calculates the optimal allocation of prospective portfolio assets such as to maximise expected return given relative to the volatility using the PyPortfolioOpt library. Once the portfolio is optimised, trades are then automatically executed through the Alpaca API. 

## Motivations/Intentions:
#### I have two main motivations behind this project:
1)	Learn more about the process of optimising portfolio allocation and the mathematics behind it.
2)	Learn about the challenges associated when creating and using a trading bot.
#### I decided to format both of the tools as classes because for the following reasons:
-	It seemed intuitive to apply a portfolio to a class object so that I could easily implement different functionality and analysis methods for different types of portfolios.
-	Improve my conceptual understanding of OOP.
Easily use portfolio and trading bot objects in other-related projects that extend the investment process outlined in this project.

## Description:
The efficient frontier is a boundary that contains portfolios with the highest expected return relative to the level of associated risk. Portfolios that lie within the boundary are sub-optimal because they are not maximising the expected return for a given level of risk.
#### An in-depth description of the PyPortfolioOpt library can be found here: https://readthedocs.org/projects/pyportfolioopt/ https://www.investopedia.com/terms/e/efficientfrontier.asp#:~:text=The%20efficient%20frontier%20is%20the,for%20the%20level%20of%20risk.

The Sharpe ratio calculates the excess return of a portfolio relative to its risk. This is calculated by subtracting the risk-free rate from the expected portfolio return and then dividing by the standard deviation of the portfolio’s excess return.
#### An in-depth description of the Sharpe Ratio and its application can be found here: https://www.investopedia.com/terms/s/sharperatio.asp

Monte Carlo simulation performs risk analysis by building models of possible results by substituting a range of values for any factor that has uncertainty. It was used in this project the expected annual portfolio returns for different annual returns. To provide the random inputs, I used a standardized normal distribution with the mean set as the current expected portfolio annual return and the standard deviation set as the volatility of expected return.
#### An in-depth description of the Monte Carlo simulation and its financial applications: https://www.palisade.com/risk/monte_carlo_simulation.asp

## Dependencies:

•	numpy
 
•	pandas
 
•	matplotlib
 
•	pandas_datareader
 
•	pypfopt
 
•	alpaca-trade-api
 
## Example: 

To use this project, you will need to make an Alpaca account (I used a paper trading account). Documentation can be found here: https://alpaca.markets/docs/api-documentation/api-v2/

#### Testing with US Tech stocks:
If we wanted to use this tool to find the optimal portfolio allocation for a group of US Tech companies we would do the following:

 - Instantiate the portfolio class:
   - assets: (str/list) ticker names of companies to analyse. E.g. 'AAPL' for Apple inc.
   - weights: (float/list) I set the initial weights to 1/len(assets) as this will be optimised in the tool.
   - start_balance: (int/float) The starting balance of the portfolio. Alpaca paper trading account allows you to start with £100000.
   - start: (date)
   - end: (date)
 
 - Run the .optimise() method:
   - optimisation_method: (str) 'max sharpe' or 'min volatility' I set the default to 'max sharpe'
   - risk-free-rate: (float) I set the default to 0.02
   
   ##### This will return portfolio summary, projections and a graph showing the historical adj. closing prices of the portfolio assets.
   # ![](images/2020-08-31%20(2).png)
   
 - Run the .monte_carlo() method:
   - time_horizon: (int) The amount of years that you expect to hold the investment for.
   - annual_additions: (int/float) Choose the amount of extra funds that will be added to the portfolio each year.
   - iterations: (int) Choose the number of iterations for the Monte Carlo method.
   - plot: (Boolean) True to plot the graph of monte carlo simulation, False otherwise.
   
   ##### This will return a summary of the Monte Carlo simulation as well as a graphical representation, should Plot=True.
   # ![](images/2020-08-31%20(3).png)
   
 - Instantiate the Alpaca trading bot:
   - api_key_id: (str) This is an api-key-id that is provided by Alpaca when you make an account.
   - secret_key: (str) This is a secret api key that is provided by Alpaca when you make an account.
   - base_url: (str) Base url that points to your account (more details in Alpaca documentation.
   
   ##### Should you decide to trade based on the information, this object then executes the trades and returns a summary of the trades. Below is a screenshot of my paper-trading a couple days after I executed my trades.
   # ![](images/2020-08-27%20(2).png)

## Challenges:
-	With the current buy-and-hold strategy implemented by the Alpaca Trading Bot, the model does not react well to external shocks. For example, the model was unable to react to the recent stock-splits of TSLA and AAPL (the test set), which resulted in an approximate 30% daily loss. I am thinking of implementing a stop-loss strategy to combat this, as well as an annualized portfolio rebalancing method.
-	Using the Yahoo Finance API, this model is dependent on a good source of data. If any data is missing, it could have a large effect on the optimal allocation and therefore portfolio performance.
## Conclusion:
Having experienced the process and application of Efficient frontiers and Monte Carlo simulations to optimise portfolios, I have confidence that these methods are fundamental in ensuring optimal returns. Creating the trading bot with Alpaca demonstrated the speed at which trades can be executed in comparison to human-performance. Nevertheless, the model does what you tell it to which means that it does not respond as a human would in extreme situations.
