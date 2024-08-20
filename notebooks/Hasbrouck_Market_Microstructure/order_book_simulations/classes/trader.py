"""
This class can be used to contain various information about the traders.
In this first iteration, it only contains the method used to place orders in the order book.

In further iterations, it could contain 
- the trader id, useful to track the orders and trades placed by each trader
- a list of orders/trades id placed by the trader
- a budget for the trader
- a risk appetite or utility function
- the number of units of stock owned by the trader (like an inventory)
- a track of the pnl of the trader
- a generalised way to describe a trading strategy followed by the trader
"""

from classes.order import Order
from classes.order_book import OrderBook
from prettytable import PrettyTable

import numpy as np

class Trader():
    def __init__(self, initial_wealth=100, number_units_stock=0, trader_id=None, check_order_feasibility=False):
        # here you can set different trader attributes
        # like the initial cash, the trading strategy type, the risk aversion, etc...
        self.wealth = initial_wealth # total wealth
        self.margin = initial_wealth # what is available to trade

        self.number_units_stock = number_units_stock
        self.trader_id = trader_id

        # do I have to check if the trader has enough cash / units to trade?
        self.check_order_feasibility = check_order_feasibility

        self.active_orders = [] # list containing the active orders of the trader (price, volume, order_id, order_type)

        self.wealth_sequence = [] # list containing tuples with (time, wealth)
        self.number_units_stock_sequence = [] # list containing tuples with (time, units stock)


    def submit_order_to_order_book(self, order_type, price, quantity, book: OrderBook, time=None, verbose=True):
        # if the order is feasible...
        if self.check_if_order_is_feasible(book, order_type, price, quantity):
            # ...generate an Order object and add it to the order book
            order = Order(order_type=order_type, price=price, quantity=quantity, trader_id=self.trader_id)

            if verbose:
                order.print_order()


            book.order_manager(order, self, time)

            self.update_active_orders(book)


    def update_active_orders(self, book):
        active_limit_buys = [(bid[0], bid[1], bid[2], 'limit_buy') for bid in book.bids if bid[3] == self.trader_id ]
        active_limit_sells = [(ask[0], ask[1], ask[2], 'limit_sell') for ask in book.asks if ask[3] == self.trader_id ]

        self.active_orders = active_limit_buys + active_limit_sells


    def print_active_orders(self, time=None):
        print(self.active_orders)
        if time is None:
            print(f"\nActive orders of trader {self.trader_id}")
        else:
            print(f"\nActive orders of trader {self.trader_id} at time {self.time}")

        table = PrettyTable()
        table.field_names = ['price', 'quantity', 'order_id', 'order_type']

        for (price, quantity, order_id, order_type) in self.active_orders:
            table.add_row((price, quantity, order_id, order_type))

        print(table)
        print("")


    def check_if_order_is_feasible(self, book, order_type, price, quantity):
        if self.check_order_feasibility:
            # logic to check
            if order_type in ('market_buy', 'limit_buy'):
                if order_type == 'market_buy':
                    price = book.asks[0][0]

                if self.margin >= price * quantity:
                    # the trader has enough money
                    return True
                else:
                    return False
                
            elif order_type in ('market_sell', 'limit_sell'):
                if self.number_units_stock >= quantity:
                    # the trader has enough shares to sell
                    return True
                else:
                    return False
            
            elif order_type in ('modify_limit_buy', 'modify_limit_sell'):
                if order_type == 'modify_limit_buy':
                    o = 'limit_buy'
                elif order_type == 'modify_limit_sell':
                    o = 'limit_sell'
                active_limit = [order for order in self.active_orders if order[3] == o]
                volume_of_orders_with_right_price = [order[1] for order in active_limit if order[0] == price]
                
                if sum(volume_of_orders_with_right_price) >= quantity:
                    return True
                else:
                    return False

            else:
                return True

            
        else:
            # if you don't have to check for feasibility, then the order is always feasible!
            return True
        
    
