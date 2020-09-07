import numpy as np
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt
import matplotlib as mpl
import indicators
import sim

mpl.style.use(['dark_background'])

def plot(data):
  fig, ax = plt.subplots()
  ax2 = ax.twinx()

  data = data.iloc[-24 * 500:-24 * 250]
  close = data['close']
  x = data.index

  upper, lower, sma = indicators.bollinger(close, window=30, std_mul=2.0)
  sell, buy = indicators.bollinger_signals(close, upper, lower)
  print('simulating')
  balance, returns, live_returns = sim.trade(data, sell, buy)
  print('plotting')

  # indicator chart
  ax.fill_between(x, upper, lower, color='darkslategray')
  ax.plot(x, close, color='springgreen', lw=1)
  ax.plot(x, sma, color='turquoise', lw=1)

  ax2.yaxis.set_major_formatter(FormatStrFormatter('%g'))

  # ax2.plot(x, balance, color='gold', lw=1)
  for y in live_returns:
    ax2.plot(x, y, color='gold', alpha=0.1, lw=1)

  # signals
  ax.scatter(x[buy], close[buy], color='green', marker=10)
  ax.scatter(x[sell], close[sell], color='crimson', marker=11)

  # plt.ylim((min(0.0, np.min(balance)), np.max(balance)))

  fig.autofmt_xdate()

  plt.show()
