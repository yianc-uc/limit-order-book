from lob import LOB
from order import order

# Some notes
# (1) The bid price should be strictly smaller than the ask price, o.w. the order will be automatically fulfilled
# (2) Now deletion doesn't work because we need to set up the parent for each node during operations

book = LOB()

orders = [
            order(id=1, time=1, is_sell=False, quantity=5, price=100),
            order(id=2, time=2, is_sell=False, quantity=5, price=95),
            order(id=3, time=3, is_sell=False, quantity=5, price=90),
            order(id=4, time=4, is_sell=True, quantity=5, price=200),
            order(id=5, time=5, is_sell=True, quantity=5, price=205),
            order(id=6, time=6, is_sell=True, quantity=5, price=210),
            ]

# (1) Test for adding new orders
for od in orders:
    book.process(od)
    
print(book.best_ask.price)
print(book.best_bid.price)

# Test
print(book.best_bid)

# (2) Test for deleting order
book.process(order(id=1, time=7, is_sell=False, quantity=0, price=100))
print(book.best_bid.price)