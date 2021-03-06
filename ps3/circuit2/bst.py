class BSTNode:
    def __init__(self, key):
        self.key = key
        self.size = 1
        self.height = 0
        self.disconnect()

    def disconnect(self):
        self.parent = None
        self.left = None
        self.right = None


def size(node):
    """ Returns the size of the tree rooted at node

        Args:
            node: root of the tree whose size is being determined
    """
    if node is None:
        return 0
    else:
        return node.size


def update_size(node):
    node.size = size(node.right) + size(node.left) + 1


class BST:

    def __init__(self):
        self.root = None

    def check_rep(self, root):
        lsize = size(root.left)
        rsize = size(root.right)
        if root.size is not lsize + rsize + 1:
            raise RuntimeError("BST Rep invalidated by size")

        lkey = root.left.key if root.left is not None else None
        rkey = root.right.key if root.right is not None else None
        if lkey > root.key or rkey < root.key:
            raise RuntimeError("BST propery invalid")
        if root.left:
            self.check_rep(root.left)
        if root.right:
            self.check_rep(root.right)

    @staticmethod
    def in_order_walk(root, result):
        if root is None: return
        left_size, right_size = 0, 0
        if root.left:
            left_size = size(root.left)
            BST.in_order_walk(root.left, result)
        result.append(root.key)
        if root.right:
            right_size = size(root.right)
            BST.in_order_walk(root.right, result)

        assert size(root) == right_size + left_size + 1

    def insert(self, key):
        """Adds key to the BST

           Args:
               key: value being added to the tree
        """
        node = BSTNode(key)

        if self.root is None:
            # Tree is empty
            self.root = node
        else:
            current = self.root
            while True:
                if node.key < current.key:
                    if current.left is None:
                        current.left = node
                        node.parent = current
                        break
                    current = current.left
                else:
                    if current.right is None:
                        current.right = node
                        node.parent = current
                        break
                    current = current.right

        # Update the size
        current = node
        while current is not None:
            update_size(current)
            current = current.parent

        return node

        # self.check_rep(self.root)

    def find(self, key):
        """Return the node for key if is in the tree, or None otherwise.
           Args:
               key: value being searched for
        """

        x = self.root

        while x is not None:
            if key > x.key:
                x = x.right
            elif key < x.key:
                x = x.left
            else:
                return x

        return None

    def transplant(self, x, y):
        """Swaps the location of two nodes in a tree
           Does not update the left or right child of y
        Args:

        x,y: the nodes being exchanged
        """

        if x.parent is None:  # x is the root
            self.root = y
        elif x.parent.left == x:  # x is a left child
            x.parent.left = y
        else:
            x.parent.right = y
        if y is not None:
            y.parent = x.parent

    def delete(self, node):
        """Removes key from the BST
          Args:
           node: value being removed from the tree
        """
        if node is None:
            return None, None
        original = node.parent

        if node.left is None:
            self.transplant(node, node.right)
        elif node.right is None:
            self.transplant(node, node.left)
        else:
            x = self.successor(node)
            original = x.parent
            if not x == node.right:
                self.transplant(x, x.right)
                x.right = node.right  # Move successor into the delete note's spot (right only)
                x.right.parent = x
            self.transplant(node, x)
            x.left = node.left
            x.left.parent = x
            update_size(x)

        # Update the size
        current = original
        while current is not None:
            update_size(current)
            current = current.parent
        parent = node.parent
        node.disconnect()
        return node, parent

        # self.check_rep(self.root)

    @staticmethod
    def min(x):
        """Returns the minimum element of the tree rooted at x

            Args:
            x: root of the tree
         """
        while x.left is not None:
            x = x.left
        return x

    @staticmethod
    def max(x):
        """Returns the maximum element of the tree rooted at x

            Args:
            x: root of the tree
         """

        while x.right is not None:
            x = x.right
        return x

    def successor(self, x):
        """ Returns the node with the smallest key greater than x.key.
            Returns None if node.key is the maximum key in the tree

            Args:
                x: node for which the successor is being found
        """

        if x.right is not None:
            return self.min(x.right)

        y = x.parent

        while not y.left == x:
            x = y
            y = y.parent

        return y

    def predecessor(self, x):
        """ Returns the node with the largest key less than x.key.
            Returns None if node.key is the maximum key in the tree

            Args:
                x: node for which the predecessor is being found
        """

        if x.left is not None:
            return self.max(x.left)

        y = x.parent

        while not y.right == x:
            x = y
            y = y.parent

        return y

    def rank(self, key):
        """ computes the rank of x in the BST. In other words returns the number of nodes <= x.key + 1
        """
        current = self.root
        r = 0
        while current is not None:
            if key < current.key:
                current = current.left
            else:
                if current.left is not None:
                    r += current.left.size
                current = current.right
                r += 1

        return r

    def lca(self, low, high):
        node = self.root
        while node is not None:
            if low <= node.key <= high:
                break
            elif low < node.key:
                node = node.left
            else:
                node = node.right
        return node

    def count(self, first_key, last_key):
        """Number of keys that fall within [first_key, last_key]."""
        low = self.find(first_key)

        if low is not None:
            return self.rank(last_key) - self.rank(first_key) + 1
        else:
            return self.rank(last_key) - self.rank(first_key)

    def __str__(self):
        if self.root is None:
            return '<empty tree>'

        def recurse(node):
            if node is None:
                return [], 0, 0
            label = str(node.key) + "(s="+str(size(node))+", h=" + str(height(node)) + ")"
            left_lines, left_pos, left_width = recurse(node.left)
            right_lines, right_pos, right_width = recurse(node.right)
            middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
            pos = left_pos + middle // 2
            width = left_pos + middle + right_width - right_pos
            while len(left_lines) < len(right_lines):
                left_lines.append(' ' * left_width)
            while len(right_lines) < len(left_lines):
                right_lines.append(' ' * right_width)
            if (middle - len(label)) % 2 == 1 and node.parent is not None and \
                    node is node.parent.left and len(label) < middle:
                label += '.'
            label = label.center(middle, '.')
            if label[0] == '.':
                label = ' ' + label[1:]
            if label[-1] == '.':
                label = label[:-1] + ' '
            lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                     ' ' * left_pos + '/' + ' ' * (middle - 2) +
                     '\\' + ' ' * (right_width - right_pos)] + \
                    [left_line + ' ' * (width - left_width - right_width) +
                     right_line
                     for left_line, right_line in zip(left_lines, right_lines)]
            return lines, pos, width

        return '\n'.join(recurse(self.root)[0])


def height(node):
    if node is not None:
        return node.height
    else:
        return -1


def update_height(node):
    node.height = max(height(node.left), height(node.right)) + 1


class AVLTree(BST):

    def __init__(self):
        BST.__init__(self)

    def check_rep(self):
        root = self.root
        if root is not None:
            lheight = height(root.left)
            rheight = height(root.right)
            if height(root) is not max(lheight, rheight) + 1:
                raise(RuntimeError("AVL rep violated. Height of tree not max + 1"))

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x.parent.left == x:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

        update_size(x)
        update_size(y)

        update_height(x)
        update_height(y)
        # self.check_rep()

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right is not None:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y.parent.left == y:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x

        update_size(y)
        update_size(x)

        update_height(y)
        update_height(x)
        # self.check_rep()

    def insert(self, key):
        node = BST.insert(self, key)
        self.rebalance(node)

    def rebalance(self, node):
        while node is not None:
            update_height(node)
            if height(node.left) >= 2 + height(node.right):
                # left heavy
                if height(node.left.left) >= height(node.left.right):
                    self.right_rotate(node)
                else:
                    self.left_rotate(node.left)
                    self.right_rotate(node)
            elif height(node.right) >= 2 + height(node.left):
                if height(node.right.right) >= height(node.right.left):
                    self.left_rotate(node)
                else:
                    self.right_rotate(node.right)
                    self.left_rotate(node)
            node = node.parent

        # self.check_rep()

    def delete(self, key):
        node, parent = BST.delete(self, key)
        self.rebalance(parent)

    def find(self, key):
        return BST.find(self, key)

    def rank(self, key):
        return BST.rank(self, key)
