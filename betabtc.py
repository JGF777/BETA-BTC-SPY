import pandas as pd
import yfinance as yf

ticker = 'BTC-USD'
benchmark = 'QQQ'
startdate = '2022-01-01'

def calculate_beta(ticker, start_date, benchmark):
    # Get historical prices for the asset and SPY
    asset_prices = yf.download(ticker, start=start_date)['Adj Close']
    spy_prices = yf.download(benchmark, start=start_date)['Adj Close']

    # Convert the index of the downloaded DataFrames to a datetime object with the correct format
    asset_prices.index = pd.to_datetime(asset_prices.index).date
    spy_prices.index = pd.to_datetime(spy_prices.index).date

    # Calculate daily returns for the asset and SPY
    asset_returns = asset_prices.pct_change()[1:]
    spy_returns = spy_prices.pct_change()[1:]

    
    # subset series to include common dates
    common_dates = set(asset_returns.index) & set(spy_returns.index)
    asset_returns = asset_returns[asset_returns.index.isin(common_dates)]
    spy_returns = spy_returns[spy_returns.index.isin(common_dates)]

    print(f"{len(common_dates)} trading days as sample")

    # Calculate the covariance and variance of the asset's returns
    cov = asset_returns.cov(spy_returns)
    var = spy_returns.var()

    # Calculate the beta
    beta = cov / var

    # Calculate the volatility
    volatilityasset = asset_returns.std()*(252**0.5)
    volatilityspy = spy_returns.std()*(252**0.5)

    # Calculate the accumulated returns
    accumulated_returnsbtc = (1 + asset_returns).cumprod()
    accumulated_returnsspy = (1 + spy_returns).cumprod()

    # Calculate the correlation 
    correlation = asset_returns.corr(spy_returns)

    return beta, volatilityasset, volatilityspy, accumulated_returnsspy, accumulated_returnsbtc, correlation

#Calling the main function
beta, volatilityasset, volatilityspy, accumulated_returnsspy, accumulated_returnsbtc, correlation = calculate_beta(
																								ticker, 
																								startdate, 
																								benchmark)

#Print statements
print(f"The beta of {ticker} compared to {benchmark} is {beta:.4f}")
print(f"The volatility of {ticker} is {volatilityasset:.4f}")
print(f"The volatility of {benchmark} is {volatilityspy:.4f}")
print(f"The accumulated returns of {benchmark} are {accumulated_returnsspy[-1]}")
print(f"The accumulated returns  of {ticker} are {accumulated_returnsbtc[-1]}")
print(f"The correlation of {ticker} with {benchmark} is {correlation}")


