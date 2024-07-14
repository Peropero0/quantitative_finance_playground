from trader import Trader
from order_book import OrderBook

trader = Trader()
book = OrderBook()

trader.submit_order_to_order_book(order_type='limit_buy', price=9, quantity=15, book=book)
trader.submit_order_to_order_book(order_type='limit_buy', price=8, quantity=4, book=book)

trader.submit_order_to_order_book(order_type='limit_sell', price=11, quantity=4, book=book)
trader.submit_order_to_order_book(order_type='limit_sell', price=10, quantity=15, book=book)

book.print_order_book_state()

trader.submit_order_to_order_book(order_type='limit_buy', price=11, quantity=5, book=book, verbose=True)
trader.submit_order_to_order_book(order_type='limit_sell', price=8, quantity=5, book=book, verbose=True)

