import numpy as np

def trade(data, sell, buy):
  close = data['close'].to_numpy()
  change = data['pchange'].to_numpy()

  initial_bank = 100
  risk = 0.01

  ticks = len(close)
  trade_signals = np.where(buy, 1.0, np.where(sell, -1.0, 0.0))
  signal_index, = np.where(trade_signals != 0.0)

  starting_price = np.tile(close[signal_index].reshape(-1, 1), ticks)
  num_positions = len(signal_index)

  positions = np.zeros(shape=(num_positions, ticks))
  positions[np.arange(num_positions), signal_index] = trade_signals[signal_index]
  positions = np.add.accumulate(positions, axis=1)
  running_returns = np.cumsum(positions * change, axis = 1)
  # spent = positions * starting_price

  returns_percent = (starting_price + running_returns) / starting_price

  # stop loss & profit
  position_close = (returns_percent <= 0.8) | (returns_percent >= 1.5)
  # only first True:
  position_close_first = np.pad(np.diff(position_close), ((0, 0), (1, 0)), 'edge')

  # realized return per tick
  realized_returns = np.zeros(shape=running_returns.shape)
  realized_returns[position_close_first] = running_returns[position_close_first]

  spendable_cash = initial_bank + np.cumsum(np.sum(realized_returns, axis=0))
  take = np.cumprod(1 - np.abs(trade_signals) * risk)

  ###
  position_multiply = np.ones(shape=running_returns.shape)
  position_multiply[position_close] = 0.0
  # roll forwward, because we cannot stop loss the start of position
  position_multiply = np.pad(position_multiply, ((0,0), (1, 0)), 'edge')[:,:-1]
  position_multiply = np.minimum.accumulate(position_multiply, axis=1)

  # ???
  running_returns = np.cumsum(positions * change * position_multiply, axis = 1)
  balance = np.sum(running_returns, axis=0)

  live_returns = running_returns ##

  return balance, running_returns, live_returns
