#!/usr/bin/env python3
# Equities Trading Bot Backtester - Final Fix
# Fixed df.name error - ticker passed explicitly
# Run instructions in comments

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

MAG7 = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']

def sma(series, period):
    return series.rolling(window=period).mean()

def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def macd(close, fast=50, slow=200, signal_period=9):
    ema_fast = ema(close, fast)
    ema_slow = ema(close, slow)
    macd_line = ema_fast - ema_slow
    signal_line = ema(macd_line, signal_period)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def rsi(close, period=14):
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rsi_val = 100 - (100 / (1 + rs))
    return rsi_val

def fetch_data(ticker, period='5y'):
    data = yf.download(ticker, period=period, progress=False)
    return data

def add_indicators(df):
    df = df.copy()
    df['sma50'] = sma(df['Close'], 50)
    df['sma200'] = sma(df['Close'], 200)
    df['macd'], df['macd_signal'], df['macd_hist'] = macd(df['Close'], fast=50, slow=200, signal_period=9)
    df['rsi'] = rsi(df['Close'])
    df['vol_ma20'] = sma(df['Volume'], 20)
    return df.dropna()

def trend_following_signal(df_slice):
    buy = (df_slice['sma50'] > df_slice['sma200']) & \
          (df_slice['macd'] > df_slice['macd_signal']) & \
          (df_slice['macd'].shift(1) <= df_slice['macd_signal'].shift(1))
    sell = (df_slice['sma50'] < df_slice['sma200']) | \
           (df_slice['macd'] < df_slice['macd_signal'])
    return buy.iloc[-1], sell.iloc[-1]

def momentum_signal(df_slice):
    vol_surge = df_slice['Volume'].iloc[-1] > 1.5 * df_slice['vol_ma20'].iloc[-1]
    rsi_buy = df_slice['rsi'].iloc[-1] < 30
    macd_cross = (df_slice['macd'].iloc[-1] > df_slice['macd_signal'].iloc[-1]) & \
                 (df_slice['macd'].shift(1).iloc[-1] <= df_slice['macd_signal'].shift(1).iloc[-1])
    buy = rsi_buy and macd_cross and vol_surge
    sell = df_slice['rsi'].iloc[-1] > 70
    return buy, sell

def social_arb_signal(ticker):
    print('  Social stub: $' + ticker + ' hype score +3%')
    return True

def backtest_strategy(df, ticker):
    initial_capital = 100000.0
    risk_per_trade = 0.02
    commission = 0.001
    position = 0
    cash = initial_capital
    portfolio_values = [initial_capital]
    trades = []

    for i in range(200, len(df)):
        price = df['Close'].iloc[i].values[0]
        df_slice = df.iloc[:i+1]
        
        trend_buy, trend_sell = trend_following_signal(df_slice)
        mom_buy, mom_sell = momentum_signal(df_slice)
        soc_buy = social_arb_signal(ticker)
  # DEBUG cash removed
  # DEBUG price removed
        
        buy_signal = trend_buy or mom_buy or soc_buy
        sell_signal = trend_sell or mom_sell
        
        if buy_signal and position == 0:
            size_value = cash * risk_per_trade
            shares = max(1, int(size_value / price))
            cost = shares * price * (1 + commission)
            if cash >= cost:
                cash -= cost
                position = shares
                trades.append('BUY ' + ticker + ' ' + str(df.index[i].date()) + ' @' + str(round(price,2)) + ' (' + str(shares) + 'sh)')
        
        elif sell_signal and position > 0:
            revenue = position * price * (1 - commission)
            cash += revenue
            trades.append('SELL ' + ticker + ' ' + str(df.index[i].date()) + ' @' + str(round(price,2)) + ' (' + str(position) + 'sh)')
            position = 0
        
        port_value = cash + (position * price if position > 0 else 0)
        portfolio_values.append(port_value)
    
    final_capital = cash + (position * df['Close'].iloc[-1].values[0] * (1 - commission) if position > 0 else 0)
    total_return = (final_capital - initial_capital) / initial_capital * 100
    num_trades = len([t for t in trades if 'BUY' in t])
    
    return {
        'total_return_pct': total_return,
        'final_capital': final_capital,
        'num_trades': num_trades,
        'trades': trades[:10],
        'portfolio': portfolio_values
    }

def plot_backtest(df, results, ticker):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12), sharex=True)
    
    ax1.plot(df.index, df['Close'], label='Close', lw=1)
    ax1.plot(df.index, df['sma50'], label='SMA50', alpha=0.8)
    ax1.plot(df.index, df['sma200'], label='SMA200', alpha=0.8)
    ax1.set_title(ticker + ' Price & Trend')
    ax1.legend()
    
    ax2.plot(df.index, df['rsi'], label='RSI', color='orange')
    ax2.plot(df.index, df['macd'], label='MACD', color='blue')
    ax2.plot(df.index, df['macd_signal'], label='MACD Sig', color='red')
    ax2.axhline(30, color='g', ls='--', alpha=0.5)
    ax2.axhline(70, color='r', ls='--', alpha=0.5)
    ax2.set_title('RSI & MACD')
    ax2.legend()
    
    port = results['portfolio']
    start_idx = len(df.index) - len(port)
    ax3.plot(df.index[start_idx:], port, label='Portfolio $', color='green')
    ax3.set_title('Portfolio Growth')
    ax3.legend()
    
    plt.tight_layout()
    plt.savefig(ticker + '_backtest.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('  Plot saved: ' + ticker + '_backtest.png')

def main():
    print('Mag7 Bot Backtest (5y daily data)')
    print('Strategies: Trend (SMA/MACD 50/200), Momentum (RSI/vol), Social stub')
    
    results_summary = {}
    
    for ticker in MAG7:
        print('\n=== ' + ticker + ' ===')
        df_raw = fetch_data(ticker)
        df = add_indicators(df_raw)
        
        res = backtest_strategy(df, ticker)
        results_summary[ticker] = res
        
        print('Return: ' + str(round(res['total_return_pct'],1)) + '%')
        print('Final capital: $' + str(round(res['final_capital'],0)))
        print('Buy trades: ' + str(res['num_trades']))
        if res['trades']:
            print('Sample trades:')
            for trade in res['trades'][:3]:
                print('  ' + trade)
        
        plot_backtest(df, res, ticker)
    
    avg_return = np.mean([r['total_return_pct'] for r in results_summary.values()])
    print('\nSUMMARY: Average Mag7 return: ' + str(round(avg_return,1)) + '%')

if __name__ == '__main__':
    main()