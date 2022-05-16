from order import order, order_wrapper

class LimitPriceNode:
    """
    BST Node implementation for the limit price
    """
    def __init__(self, new_order=None) -> None:
        if new_order:
            new_wrapper = order_wrapper(new_order)
            new_wrapper.LimitPrice = self
            
            # Data contained
            self.wrapper = new_wrapper
            self.price = new_wrapper.price
        else:
            self.wrapper = None
            self.price = None
        
        # Children and parent
        self.height = 1
        self.parent = None
        self.left = None
        self.right = None
        
class AVL_Tree:
    # Recursive function to insert key in
    # subtree rooted with node and returns
    # new root of subtree.
    def insert(self, root, new_node: LimitPriceNode):
        # Step 1 - Perform normal BST
        if not root:
            return new_node
        elif new_node.price < root.price:
            root.left = self.insert(root.left, new_node)
        else:
            root.right = self.insert(root.right, new_node)
 
        # Step 2 - Update the height of the
        # ancestor node
        root.height = 1 + max(self.getHeight(root.left),
                           self.getHeight(root.right))
 
        # Step 3 - Get the balance factor
        balance = self.getBalance(root)
 
        # Step 4 - If the node is unbalanced,
        # then try out the 4 cases
        # Case 1 - Left Left
        if balance > 1 and new_node.price < root.left.price:
            return self.rightRotate(root)
 
        # Case 2 - Right Right
        if balance < -1 and new_node.price > root.right.price:
            return self.leftRotate(root)
 
        # Case 3 - Left Right
        if balance > 1 and new_node.price > root.left.price:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
 
        # Case 4 - Right Left
        if balance < -1 and new_node.price < root.right.price:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
 
        return root
    
    # Recursive function to delete a node with
    # given key from subtree with given root.
    # It returns root of the modified subtree.
    def delete(self, root, key):
 
        # Step 1 - Perform standard BST delete
        if not root:
            return root
 
        elif key < root.price:
            root.left = self.delete(root.left, key)
 
        elif key > root.price:
            root.right = self.delete(root.right, key)
 
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
 
            elif root.right is None:
                temp = root.left
                root = None
                return temp
 
            temp = self.getMinValueNode(root.right)
            root.price = temp.price
            root.right = self.delete(root.right,
                                      temp.price)
 
        # If the tree has only one node,
        # simply return it
        if root is None:
            return root
 
        # Step 2 - Update the height of the
        # ancestor node
        root.height = 1 + max(self.getHeight(root.left),
                            self.getHeight(root.right))
 
        # Step 3 - Get the balance factor
        balance = self.getBalance(root)
 
        # Step 4 - If the node is unbalanced,
        # then try out the 4 cases
        # Case 1 - Left Left
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)
 
        # Case 2 - Right Right
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)
 
        # Case 3 - Left Right
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
 
        # Case 4 - Right Left
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
 
        return root
 
    def leftRotate(self, z):
 
        y = z.right
        T2 = y.left
 
        # Perform rotation
        y.left = z
        z.right = T2
 
        # Update heights
        z.height = 1 + max(self.getHeight(z.left),
                         self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                         self.getHeight(y.right))
 
        # Return the new root
        return y
 
    def rightRotate(self, z):
 
        y = z.left
        T3 = y.right
 
        # Perform rotation
        y.right = z
        z.left = T3
 
        # Update heights
        z.height = 1 + max(self.getHeight(z.left),
                        self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                        self.getHeight(y.right))
 
        # Return the new root
        return y
 
    def getHeight(self, root):
        if not root:
            return 0
 
        return root.height
 
    def getBalance(self, root):
        if not root:
            return 0
 
        return self.getHeight(root.left) - self.getHeight(root.right)
 
    def preOrder(self, root):
 
        if not root:
            return
 
        print("{0} ".format(root.price), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)
    