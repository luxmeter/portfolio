"""
This module helps to find out how much money you have to invest
in an asset to align with a predefined distribution.
"""
import math
import datetime as dt

import pandas as pd
import pandas_datareader as pdr


def stock_price_eur(symbol):
    """Returns current price of a stock in EUR.

    Args:
        symbol (str): Identifying symbol of the stock.

    Returns:
        numpy.float64: Current stock price in EUR.
    """
    stock = pdr.get_quote_yahoo(symbol)
    currency = stock.currency.values[0]
    price = pdr.get_quote_yahoo(f"{currency.upper()}EUR=X").price.values[0]
    ratio = price if currency.upper() != "GBP" else price / 100
    return stock.price.values[0] * ratio


def current_distribution(df):
    """Calculates current distribution of the networth.

    Args:
        df (pandas.Dataframe): Dataframe providing `Stock Price` and `Shares`.

    Returns:
        pandas.Dataframe: Single dataframe providing `Current Distribution`
    """
    current_networth = (df["Stock Price"] * df["Shares"]).sum()
    distribution = (
        (df["Stock Price"] * df["Shares"])
        .apply(lambda n: n / current_networth)
        .rename("Current Distribution")
    )
    return distribution


def calc_shares_to_purchase(df, investment, order_cost=0, exclusions=None):
    """Calculates, based on your investment, how many shares you have to purchase to align with the desired distribution.
    It is possible to exclude stocks from current investment.
    In this case, the distribution of the investment is recalculated over the remaining stocks.
    A stock will be excluded automatically when its price is higher than the calculated investment.

    Args:
        df (pandas.Dataframe): Dataframe providing `Symbol`, `Desired Distribution` and `Current Distribution`.
        investment (float): How much EUR you want to invest.
        order_cost (float): How much an order cost in EUR.
        exclusions: Stocks identified by their symbol you want to exclude from the distribution.

    Returns:
        pandas.Dataframe: Copy of passed in dataframe but extended by new columns: `New Relative Distribution`, `To Invest`, `Expected Distribution`
    """

    def calc_distribution(df):
        res = pd.DataFrame()
        sum_ex_dist = sum(
            n for n in df[df["Symbol"].isin(exclusions)]["Desired Distribution"].values
        )
        ratio = 1 / (1 - sum_ex_dist)
        res["New Relative Distribution"] = [
            n * ratio if symbol not in exclusions else 0
            for symbol, n in zip(df["Symbol"].values, df["Desired Distribution"].values)
        ]
        res["To Invest"] = res["New Relative Distribution"] * (
            investment - (order_cost * (len(df) - len(exclusions)))
        )
        res = pd.concat([df.filter(["Symbol", "Stock Price"]), res], axis=1)
        return res

    above_target_dist = df[df["Current Distribution"] > df["Desired Distribution"]][
        "Symbol"
    ].values
    exclusions.extend(above_target_dist)
    new_dist = calc_distribution(df)

    too_expensive = new_dist[
        (new_dist["Stock Price"] > new_dist["To Invest"]) & (new_dist["To Invest"] > 0)
    ]["Symbol"].values
    if too_expensive.size > 0:
        exclusions.extend(too_expensive)
        new_dist = calc_distribution(df)
    df = pd.merge(df, new_dist)
    df["Shares To Purchase"] = df["To Invest"] / df["Stock Price"]
    return df
