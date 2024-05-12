"""
This file implements a simple vectorial backtest class.
You can import the class in any python file and perform a simple backtest using the class method do_backtest.
This method uses the prices of instruments of the investable universe and each instrument signal to perform a backtest.

Signals are meant to be high numbers for assets that I want to buy and low numbers for assets that I want to sell.
Find an example in the notebook 'simple_vectorial_backtest.ipynb'.

The backtest is equally weighted, meaning that, for each leg, every instrument weights the same.

The arguments of the constructor are:
- signals: pd.DataFrame indexed by datetime and asset and with a column called 'signal' with strategy signals
- prices: pd.DataFrame indexed by datetime. The columns are the asset prices
- initial_cash: a float that represents the initial value of the equity line
- commissions: a float representing how many basis points a transaction costs
- number_of_instruments_long_leg: int representing how many instruments to go long
- number_of_instruments_short_leg: int representing how many instruments to go short. If this number is 0 then the strategy is long only.

The weights of the long only strategy sum to 1, the weights of the long short strategy sum to 0 and their absolute value sums to 1.
This is done in order to keep the leverage at 1.

"""

import pandas as pd
import numpy as np

class VectorialBacktest():

    # constructor
    def __init__(
            self, 
            signals, 
            prices, 
            initial_cash, 
            commissions, 
            number_of_instruments_long_leg, 
            number_of_instruments_short_leg) -> None:
        
        self.signals = signals
        self.prices = prices
        self.initial_cash = initial_cash
        self.commissions = commissions
        self.number_of_instruments_long_leg = number_of_instruments_long_leg
        self.number_of_instruments_short_leg = number_of_instruments_short_leg

    # define if the strategy is long short or long only
    def is_longshort(self):
        if self.number_of_instruments_short_leg > 0:
            return True # the strategy is long short, i.e. we go long some instruments and short some others
        else:
            return False # the strategy is long only, i.e. I can only have positive weights allocated
    
    # get the instruments belonging to the long leg and compute their weights.
    # the strategy assigns equal weights to each instrument
    def get_long_leg_instruments_weights(self):
        long_leg = pd.DataFrame(self.signals['signal'].groupby(level='datetime').nlargest(self.number_of_instruments_long_leg).droplevel(0))
        
        if self.is_longshort():
            multiplier = 2 # done to keep the leverage to 1 in long short
        else:
            multiplier = 1

        # assign equal weights
        long_leg['signal'] = 1 / (multiplier * self.number_of_instruments_long_leg) 
        return long_leg

    # get the instruments belonging to the short leg and compute their weights.
    # the strategy assigns equal weights to each instrument
    def get_short_leg_instruments_weights(self):
        short_leg =  pd.DataFrame(self.signals['signal'].groupby(level='datetime').nsmallest(self.number_of_instruments_short_leg).droplevel(0))
        
        if self.is_longshort():
            # assign equal weights
            short_leg['signal'] = - 1 / (2 * self.number_of_instruments_short_leg) 
        else:
            short_leg['signal'] = 0

        return short_leg

    # compute the metrics maximum drawdown, that is the portfolio maximum loss from a peak before a new peak happens.
    @staticmethod
    def _compute_max_drawdown(equity_line):
        peak = -np.inf  # Initialize peak value
        drawdown = 0     # Initialize drawdown value
        max_drawdown = 0 # Initialize maximum drawdown value

        for i in range(len(equity_line)):
            if equity_line[i] > peak:
                peak = equity_line[i]
            else:
                drawdown = (peak - equity_line[i]) / peak
                if drawdown > max_drawdown:
                    max_drawdown = drawdown

        return max_drawdown

    # compute backtest metrics
    @staticmethod
    def _compute_metrics(trades_df, equity_line_df):
        cumulative_return = equity_line_df.iloc[-1]['portfolio_value'] / equity_line_df.iloc[0]['portfolio_value'] - 1
        annualised_return = equity_line_df['portfolio_value'].pct_change().mean() * 252
        annualised_std = equity_line_df['portfolio_value'].pct_change().std() * np.sqrt(252)
        sharpe = annualised_return / annualised_std
        max_drawdown = VectorialBacktest._compute_max_drawdown(equity_line_df['portfolio_value'].values)
        calmar = annualised_return / abs(max_drawdown)

        return  {
            'cumulative_return': cumulative_return,
            'annualised_return': annualised_return,
            'annualised_std': annualised_std,
            'sharpe': sharpe,
            'max_drawdown': max_drawdown,
            'calmar': calmar,
        }



    def do_backtest(self):
        # sort signals dataframe to get the top n and bottom n signals
        top_n = self.get_long_leg_instruments_weights()
        bottom_n = self.get_short_leg_instruments_weights()

        # create portfolio weights dataframe
        portfolio_weights_df = pd.concat([top_n, bottom_n])
        portfolio_weights_df = portfolio_weights_df['signal'].unstack()
        portfolio_weights_df = portfolio_weights_df.fillna(0)  # Fill NaNs with 0s

        # compute forward returns for each asset
        # this is done in order to compute the daily pnl
        fwd_returns_df = self.prices.pct_change().shift(-1)

        # commissions
        transaction_costs = self.commissions / 10000  # Convert basis points to decimal


        # now do the backtest
        # first instantiate the dataframe containing the necessary info
        portfolio_value = pd.DataFrame()

        # compute the weights change with relation to the last period
        weights_change = portfolio_weights_df.diff().fillna(0)

        # set the first change as the actual weights.
        weights_change.iloc[0] = portfolio_weights_df.iloc[0]

        # now compute the absoulte sum of weights difference, useful to compute commissions 
        sum_of_absolute_weights_difference = abs(weights_change).sum(axis=1)

        # the gross return of the period is 1 + the sum of weight multiplied by fwd returns
        # notice that these returns happen at the end of the next bar, so they happen in the future
        # we should shift our final equity line by 1 bar in the future
        # we will do this at the end of the computation
        portfolio_value['gross_return'] = 1 + (portfolio_weights_df * fwd_returns_df).sum(axis=1)

        # compute the daily costs in percentage
        portfolio_value['daily_percentage_costs'] = sum_of_absolute_weights_difference * transaction_costs
        
        # and the gross daily costs
        portfolio_value['gross_daily_percentage_costs'] = 1 - portfolio_value['daily_percentage_costs']

        # the total return in percentage is the gross return multiplied by gross costs
        portfolio_value['total_return'] = portfolio_value['gross_return'] * portfolio_value['gross_daily_percentage_costs']
        
        # then we can obtain our equity line by computing the total return for each datapoint
        # and multiplying by initial cash. Moreover we shift the curve, as discussed previously
        portfolio_value = portfolio_value.shift()
        portfolio_value['portfolio_value'] = portfolio_value['total_return'].cumprod() * self.initial_cash
        portfolio_value.loc[portfolio_value.index[0], 'portfolio_value'] = self.initial_cash

        # compute metrics
        backtest_metrics = VectorialBacktest._compute_metrics(portfolio_weights_df, 
                                                              portfolio_value[['portfolio_value']] 
                                                              )

        return portfolio_weights_df, portfolio_value[['portfolio_value']], backtest_metrics
