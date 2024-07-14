from order import Order
from order_book import OrderBook

class Trader():
    def __init__(self):
        # here you can set different trader attributes
        # like the initial cash, the trading strategy type, the risk aversion, etc...
        #self.cash = initial_cash
        #self.trader_id = trader_id
        pass

    def submit_order_to_order_book(self, order_type, price, quantity, book: OrderBook, verbose=False):
        order = Order(order_type=order_type, price=price, quantity=quantity)
        book.add_order_to_the_order_book(order)

        if verbose:
            print("\nAdding the following order:")
            print(f"order type: {order_type}, price: {price}, quantity: {quantity}\n")
            book.print_order_book_state()

        return book
