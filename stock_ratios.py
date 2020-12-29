import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rcParams
import numpy as np
import pandas as pd
from datetime import date

from constants import cash

from currency_converter import CurrencyConverter
c = CurrencyConverter()
# print(c.convert(100, 'EUR', 'USD'))

today = date.today()

rcParams.update({'font.sans-serif': 'Arial'})

def trim_data():
    df = pd.read_csv('data/quotes.csv')
    print(f'{df}')
    df.to_csv(f'data/quotes_{today}.csv')

    df = df.drop(columns=['Date', 'Time', 'Change', 'Open', 'High', 'Low', 'Volume', 'Trade Date', 'Commission', 'High Limit', 'Low Limit', 'Comment'])
    df = df.dropna()

    print(df)

    for index, row in df.iterrows():
        price = row['Current Price']
        quantity = row['Quantity']

        df.loc[index, 'Purchased Amount'] = round(price * quantity)

    cash = c.convert(cash, 'DKK', 'USD')
    stocks = df.groupby('Symbol')['Purchased Amount'].sum()
    stocks = stocks.append(pd.Series(cash, index=['CASH']))

    return stocks

def plot(stock_ratios, tickers):
    background_color = '#1C2024'
    grid_color = '#444444'
    c_orange = '#F2B134'
    c_red = '#ED553B'
    c_white = '#FFFFFF'
    c_green = '#62BF04'

    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor(background_color)

    ax.set_facecolor(background_color)
    ax.tick_params(colors=c_white)
    ax.xaxis.label.set_color(c_white)
    ax.yaxis.label.set_color(c_white)
    ax.grid(True, color=grid_color)

    y_pos = np.arange(len(stock_ratios))

    ax.bar(y_pos, stock_ratios, color=c_red)
    plt.xticks(y_pos, tickers)

    plt.title('Stock Ratios', color=c_white)

    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    plt.savefig(f'plots/stockratios_{today}.png', facecolor=background_color)


def data_preprocessing(stocks):
    stock_ratios = []
    tickers = []

    stocks = {key: value for key, value in sorted(stocks.items(), key=lambda item: item[1], reverse=True)}

    total = 0
    for key, item in stocks.items():
        total += item

    for ticker, value in stocks.items():
        tickers.append(ticker)
        stock_ratios.append(value / total * 100)

    return stock_ratios, tickers

def main():
    stocks = trim_data()
    stock_ratios, tickers = data_preprocessing(stocks)
    plot(stock_ratios, tickers)

if __name__ == '__main__':
    main()