from sortedcontainers import SortedDict

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
    
    def set_quantity(self, new_quant):
        self._quantity = new_quant
        
    def append(self, new_order):
        self.next_order = new_order
        new_order.prev_order = self
        
    def pop(self):
        # Detach the order from the linked list
        if not self.prev_order and not self.next_order:
            # This is the only order in the LimitPrice node
            self.wrapper.order_head = None
            self.wrapper.order_tail = None
            self.wrapper.total_size = 0
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
            self._quantity = new_order.quantity
        

class order_wrapper:
    """
    Wrapper of the doubly-linked list for order. It contains information about the head, tail, total_size, etc.
    """
    def __init__(self, new_order: order) -> None:
        # Initialize an order wrapper using a new order for the limit price
        self.order_head = new_order
        self.order_tail = new_order
        self.total_size = new_order.quantity
        self.price      = new_order.price
        new_order.wrapper = self
        
    def empty(self):
        return True if self.total_size == 0 else False
        
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
    
class LOB:
    def __init__(self) -> None:
        self.bid_tree = SortedDict()
        self.ask_tree = SortedDict()
        self.best_ask = float('inf')
        self.best_bid = -float('inf')
        self.order_dict = {}
        
    def process(self, new_order: order):
        if new_order.id in self.order_dict:
            # This is an existing order
            if new_order.quantity == 0:
                # Remove the order
                self.order_dict[new_order.id].pop()
                del self.order_dict[new_order.id]
                if new_order.is_sell and self.ask_tree[new_order.price].empty():
                    # Need to remove the current price level
                    del self.ask_tree[new_order.price]
                elif not new_order.is_sell and self.bid_tree[new_order.price].empty():
                    del self.bid_tree[new_order.price]
            else:
                # Update order
                self.order_dict[new_order.id].update(new_order)
        else:
            # New order
            self.order_dict[new_order.id] = new_order
            if new_order.is_sell and new_order.price in self.ask_tree:
                # The price level exists
                self.ask_tree[new_order.price].append(new_order)
            elif not new_order.is_sell and new_order.price in self.bid_tree:
                # The price level exists
                self.bid_tree[new_order.price].append(new_order)
            else:
                new_wrapper = order_wrapper(new_order)
                if new_order.is_sell:
                    self.ask_tree[new_order.price] = new_wrapper
                else:
                    self.bid_tree[new_order.price] = new_wrapper
                    
        # Update the best ask and bid price
        self.best_ask = self.ask_tree.peekitem(0)[0] if len(self.ask_tree)>0 else self.best_ask
        self.best_bid = self.bid_tree.peekitem(-1)[0] if len(self.bid_tree)>0 else self.best_bid
                    
    def __str__(self):
        ret = ''
        ret = ret + 'BUY ORDER' + ('-'*20) + '\n'
        if len(self.bid_tree) == 0:
            ret += 'Buy order is empty\n'
        else:
            for key,val in self.bid_tree.items():
                ret += "Price: " + str(key) + ", Quantity: " + str(val.total_size) + "\n"
        
        ret = ret + 'SELL ORDER' + ('-'*20) + '\n'
        if len(self.ask_tree) == 0:
            ret += 'Sell order is empty\n'
        else:
            for key,val in self.ask_tree.items():
                ret += "Price: " + str(key) + ", Quantity: " + str(val.total_size) + "\n"
        
        ret += ("Summary: The best ask price is " + str(self.best_ask) + " and the best bid price is " \
            + str(self.best_bid) + "\n")
        
        return ret