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

from order import Order
from order_book import OrderBook

class Trader():
    def __init__(self):
        # here you can set different trader attributes
        # like the initial cash, the trading strategy type, the risk aversion, etc...
        #self.cash = initial_cash
        #self.trader_id = trader_id
        pass

    def submit_order_to_order_book(self, order_type, price, quantity, book: OrderBook):
        # generate an Order object and add it to the order book
        order = Order(order_type=order_type, price=price, quantity=quantity)

        order.print_order()

        book.add_order_to_the_order_book(order)
