import sys
import numpy as np
import pandas as pd

np.set_printoptions(
  precision=4,
  suppress=True,
  threshold=sys.maxsize,
)

def simple_moving_average(a, window):
  x = np.convolve(a, np.ones(window), 'valid') / window
  return np.pad(x, (window - 1, 0), constant_values=(np.nan))

def bollinger(close, window, std_mul = 1):
  sma = simple_moving_average(close, window)
  std = close.rolling(window=window).std()

  upper_band = sma + std * std_mul
  lower_band = sma - std * std_mul

  return upper_band, lower_band, sma

# orders based on oversold / overbought indicators
def bollinger_signals(close, upper_band, lower_band):
  sell = close > upper_band
  buy = close < lower_band
  return sell, buy
