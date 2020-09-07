import pandas as pd
import numpy as np
from pprint import pprint
from checkpointer import checkpoint

import indicators
import plot

@checkpoint
def get_ohlc():
  print('reading data..')
  data = pd.read_csv('./data/bitstampUSD.csv', names=['timestamp', 'price', 'volume'], header=None)

  print('transforming data')

  data['date'] = pd.to_datetime(data['timestamp'], unit='s')
  data = data.set_index('date', drop=True).resample('60Min')

  # bfill: backwards-fill non-traded hours with previous close
  ohlc = data['price'].ohlc().bfill()
  out = ohlc
  out['volume'] = data['volume'].sum()
  out['change'] = out['close'] / np.roll(out['close'], 1) - 1
  out['pchange'] = out['close'] - np.roll(out['close'], 1)
  out['pchange'][0] = 0.0
  # out['change'][0] = 0.0

  return out

if __name__ == '__main__':
  data = get_ohlc()
  plot.plot(data)
