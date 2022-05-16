# Define the order class
class order:
    def __init__(self, id, time, price, quantity, is_sell, prev_order=None, next_order=None,\
        wrapper=None) -> None:
        # Order attributes
        # Private attributes
        self._id = id
        self._time = time 
        self._price = price
        self._quantity = quantity
        self._is_sell = is_sell
        
        # Neighbors
        self.prev_order = prev_order
        self.next_order = next_order
        self.wrapper = wrapper
        
    @property
    def id(self):
        return self._id
    
    @property
    def price(self):
        return self._price
    
    @property
    def is_sell(self):
        return self._is_sell
        
    @property
    def quantity(self):
        return self._quantity
        
    def append(self, new_order):
        self.next_order = new_order
        new_order.prev_order = self
        
    def pop(self):
        # Detach the order from the linked list
        if not self.prev_order and not self.next_order:
            # This is the only order in the LimitPrice node
            pass
        elif self.prev_order and not self.next_order:
            # This is the last order
            self.prev_order.next_order = None
            self.wrapper.order_tail = self.prev_order
            self.wrapper.total_size -= self.quantity
        elif not self.prev_order and self.next_order:
            # This is the first order
            self.prev_order.prev_order = None
            self.wrapper.order_head = self.next_order
            self.wrapper.total_size -= self.quantity
        else:
            # This is an order in the middle
            self.prev_order.next_order = self.next_order
            self.next_order.prev_order = self.prev_order
            self.wrapper.total_size -= self.quantity
            
    def update(self, new_order):
        assert self.price == new_order.price, "Order price doesn't match, maybe the order id is wrong"
        assert self.is_sell == new_order.is_sell, "Order type doesn't match, maybe the order id is wrong"
        self._time = new_order._time 
        if self.quantity == new_order.quantity:
            # Nothing different
            pass
        else:
            self.wrapper.total_size = self.wrapper.total_size - self.quantity + new_order.quantity
            self.quantity = new_order.quantity
        

class order_wrapper:
    """
    Wrapper of the doubly-linked list for order. It contains information about the head, tail, total_size, etc.
    """
    def __init__(self, new_order: order) -> None:
        self.LimitPrice = None
        self.order_head = new_order
        self.order_tail = new_order
        self.total_size = new_order.quantity
        self.price      = new_order.price
        
    def append(self, new_order: order):
        # The order belongs to the wrapper
        new_order.wrapper = self
        if not self.order_head:
            # First order
            self.order_head = new_order
            self.order_tail = new_order
            self.total_size = new_order.quantity
            self.price      = new_order.price
        else:
            assert self.price == new_order.price, "The new order's price doesn't match with the group"
            self.order_tail.append(new_order)
            self.order_tail = self.order_tail.next_order
            self.total_size += new_order.quantity
    