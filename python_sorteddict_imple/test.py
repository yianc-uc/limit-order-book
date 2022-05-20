from lob import *

# Test with adding orders
orders = [
            order(id=1, is_sell=True, quantity=5, price=100, time=1),
            order(id=2, is_sell=True, quantity=5, price=95, time=1),
            order(id=3, is_sell=True, quantity=5, price=90, time=1),
            order(id=4, is_sell=False, quantity=5, price=200, time=1),
            order(id=5, is_sell=False, quantity=5, price=205, time=1),
            order(id=6, is_sell=False, quantity=5, price=210, time=1),
            ]

book = LOB()
for ord in orders:
    book.process(ord)
    
print(book)

# Test with deleting orders
book.process(order(id=3, is_sell=True, quantity=0, price=90, time=2))
print(book)

# Test with updating orders
book.process(order(id=2, is_sell=True, quantity=10, price=95, time=3))
print(book)
