"""
This class contains the orders details, like the order type, the price and the quantity.
It can be furtherly expanded with attributes like the order id and the trader that submitted the order. 
"""
class Order():

    supported_orders = (
        'market_buy',
        'market_sell',
        'limit_buy',
        'limit_sell',
        'do_nothing')

    def __init__(self, order_type, price, quantity):

        if order_type not in self.supported_orders:
            raise ValueError(f'valid values for order_type are {self.supported_orders}.\nYou passed {order_type}')
            
        self.order_type = order_type

        # other checks:
        # price > 0, quantity > 0, if market_order you should pass no prices, if limit you should pass it
        self.price = price
        self.quantity = quantity

        # add the attribute order id if you want to implement the cancel order feature  

    def print_order(self):
        print(f"{self.order_type} - price: {self.price} - quantity: {self.quantity}")

