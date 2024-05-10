import pandas as pd
import numpy as np

class VectorialBacktest():
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

    def is_longshort(self):
        if self.number_of_instruments_short_leg > 0:
            return True
        else:
            return False
    
    def get_long_leg_instruments_weights(self):
        long_leg = pd.DataFrame(self.signals['signal'].groupby(level='datetime').nlargest(self.number_of_instruments_long_leg).droplevel(0))
        
        if self.is_longshort():
            multiplier = 2
        else:
            multiplier = 1

        long_leg['signal'] = 1 / (multiplier * self.number_of_instruments_long_leg) 
        return long_leg

    def get_short_leg_instruments_weights(self):
        short_leg =  pd.DataFrame(self.signals['signal'].groupby(level='datetime').nsmallest(self.number_of_instruments_short_leg).droplevel(0))
        
        if self.is_longshort():
            short_leg['signal'] = - 1 / (2 * self.number_of_instruments_short_leg) 
        else:
            short_leg['signal'] = 0

        return short_leg

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

    @staticmethod
    def _compute_metrics(trades_df, equity_line_df, total_commissions):
        annualised_return = equity_line_df['portfolio_value'].pct_change().mean() * 252
        annualised_std = equity_line_df['portfolio_value'].pct_change().std() * np.sqrt(252)
        sharpe = annualised_return / annualised_std
        max_drawdown = VectorialBacktest._compute_max_drawdown(equity_line_df['portfolio_value'].values)
        calmar = annualised_return / abs(max_drawdown)

        return  {
            'annualised_return': annualised_return,
            'annualised_std': annualised_std,
            'sharpe': sharpe,
            'max_drawdown': max_drawdown,
            'calmar': calmar,
            'total_commissions': total_commissions
        }



    def do_backtest(self):
        # Sort signals dataframe to get the top n and bottom n signals
        top_n = self.get_long_leg_instruments_weights()
        bottom_n = self.get_short_leg_instruments_weights()

        # Create trade signals dataframe
        trades_df = pd.concat([top_n, bottom_n])
        trades_df = trades_df['signal'].unstack()
        trades_df = trades_df.fillna(0)  # Fill NaNs with 0s

        # Calculate transaction costs
        transaction_costs = self.commissions / 10000  # Convert basis points to decimal
        
        # Initialize DataFrame to store portfolio returns
        equity_line = []
        total_commissions = 0

        # Initialize cash balance
        portfolio_value = self.initial_cash
        fwd_returns_df = self.prices.pct_change().shift(-1)

        # Loop through each datetime
        for i in range(len(self.prices.index) - 1):
            datetime = fwd_returns_df.index[i]
            equity_line.append(pd.DataFrame({'portfolio_value': [portfolio_value]}, index=[datetime]))


            # Get weights for current datetime
            weights = trades_df.loc[datetime]

            if i == 0:
                previous_weights = pd.Series(np.zeros(weights.size), index=weights.index)
            else:
                previous_weights = trades_df.loc[fwd_returns_df.index[i-1]]
            
            # total weights difference
            sum_of_absolute_weights_difference = abs(weights - previous_weights).sum()

            # compute the transaction costs
            daily_costs = sum_of_absolute_weights_difference * transaction_costs * portfolio_value

            # subtract them from portfolio value
            portfolio_value -= daily_costs
            total_commissions += daily_costs
            
            # daily forward returns
            fwd_returns = fwd_returns_df.loc[datetime]

            # total portfolio return
            total_return = (weights * fwd_returns).sum()

            # apply the return to the portfolio, after acconting for costs
            portfolio_value *= 1 + total_return

        equity_line.append(pd.DataFrame({'portfolio_value': [portfolio_value]}, index=[datetime]))

        # Convert executed trades list to DataFrame
        equity_line_df = pd.concat(equity_line)
        equity_line_df.index = equity_line_df.index.rename('datetime')

        backtest_metrics = VectorialBacktest._compute_metrics(trades_df, equity_line_df, total_commissions)

        return trades_df, equity_line_df, backtest_metrics
