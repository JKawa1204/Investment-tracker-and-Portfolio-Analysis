# backend/utils/avl_tree.py
class AVLNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if not node:
            return AVLNode(key, data)
        
        if key < node.key:
            node.left = self._insert(node.left, key, data)
        else:
            node.right = self._insert(node.right, key, data)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return self._balance(node)

    def in_order_traversal(self):
        results = []
        self._in_order(self.root, results)
        return results

    def _in_order(self, node, results):
        if node:
            self._in_order(node.left, results)
            results.append(node.data)
            self._in_order(node.right, results)

    def _balance(self, node):
        # Add balancing logic
        return node
