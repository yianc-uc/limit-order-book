from limit_price import LimitPriceNode, AVL_Tree
from order import order, order_wrapper

class LOB:
    
    def __init__(self) -> None:
        self.ask_tree = None
        self.bid_tree = None
        self.best_ask = None
        self.best_bid = None
        self.ask_tree_self = AVL_Tree()
        self.bid_tree_self = AVL_Tree()
        self._order_dict = {}
        self._price_dict = {}
        
    def process(self, new_order: order):
        ## Need also to update _order_dict and _price_dict
        if new_order.id in self._order_dict:
            # Order currently in the record
            if new_order.quantity == 0:
                # Remove order
                if not self._order_dict[new_order.id].prev_order and not self._order_dict[new_order.id].next_order:
                    # Need also to delete the limit price node
                    if new_order.is_sell:
                        # Update the best ask
                        if self.best_ask.price == new_order.price:
                            self.best_ask = self._price_dict[new_order.price].parent if self._price_dict[new_order.price].parent else None
                        self.ask_tree = self.ask_tree_self.delete(self.ask_tree, new_order.price)
                    else:
                        # Update the best bid
                        if self.best_bid.price == new_order.price:
                            self.best_bid = self._price_dict[new_order.price].parent if self._price_dict[new_order.price].parent else None
                        self.bid_tree = self.bid_tree_self.delete(self.bid_tree, new_order.price)
                    
                    del self._price_dict[new_order.price]
                else: 
                    self._order_dict[new_order.id].pop()
                
                del self._order_dict[new_order.id]
            else:
                # Update order
                self._order_dict[new_order.id].update(new_order)
        else:
            # New order
            if new_order.price in self._price_dict:
                # The LimitPriceNode exists
                self._price_dict[new_order.price].wrapper.append(new_order)
                self._order_dict[new_order.id] = new_order
            else:
                # The LimitPriceNode doesn't exist
                new_node = LimitPriceNode(new_order)
                if not new_order.is_sell:
                    # A new sell order
                    self.best_bid = new_node if (self.best_bid is None or self.best_bid.price<new_node.price) else self.best_bid
                    self.bid_tree = self.bid_tree_self.insert(self.bid_tree, new_node)
                else:
                    # A new buy order
                    self.best_ask = new_node if (self.best_ask is None or self.best_ask.price>new_node.price) else self.best_ask
                    self.ask_tree = self.ask_tree_self.insert(self.ask_tree, new_node)
                
                self._price_dict[new_order.price] = new_node
                self._order_dict[new_order.id] = new_order