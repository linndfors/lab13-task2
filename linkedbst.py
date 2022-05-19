"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log2
import random
import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            res_string= ""
            if node != None:
                res_string+= recurse(node.right, level + 1)
                res_string+= "| " * level
                res_string+= str(node.data) + "\n"
                res_string+= recurse(node.left, level + 1)
            return res_string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the _root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                item_removed = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                new_child = currentNode.right

                # Case 3: The node has no right child
            else:
                new_child = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the _root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if self._root is None:
                return 0
            if top.left == None and top.right == None:
                return 0
            else:
                if top.right != None:
                    right_move = height1(top.right)
                else:
                    right_move = 0
                if top.left != None:
                    left_move = height1(top.left)
                else:
                    left_move = 0
                return max(right_move, left_move) + 1
        return height1(self._root)
    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * log2(len(list(self.inorder()))+1) -1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        res = []
        list_of_elems = list(self.inorder())
        for elem in list_of_elems:
            if low <= elem <= high:
                res.append(elem)
        return res

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def helper(elems):
            elems = list(elems)
            if len(elems) == 0:
                return
            middle = len(elems)//2
            node = BSTNode(elems[middle])
            node.left = helper(elems[:middle])
            node.right = helper(elems[middle + 1:])
            return node
        self._root = helper(self.inorder())
    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for elem in list(self.inorder()):
            if elem > item:
                return elem
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        list_of_elems = list(self.inorder())
        list_of_elems.reverse()
        for elem in list_of_elems:
            if elem < item:
                return elem
        return None
        
    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        def basic_find(contain, index):
            return contain[index]
        # def binary_sorted_tree(contain, word):
        #     ind = contain.find(word)
        #     return ind

        def binary_tree(contain, word):
            ind = contain.find(word)
            return ind

        # def balanced_binary_tree(contain, word):
        #     ind = contain.find(word)
        #     return ind

        with open(path, "r") as data:
            words = data.read().splitlines()[:1000]
        

        def create_tree(list_of_words):
            sorted_tree = LinkedBST()
            for word in list_of_words:
                sorted_tree.add(word)
            return sorted_tree
        
        start = time.time()
        for ind in range(10000):
            random_ind = random.randint(0, len(words) - 1)
            basic_find(words, random_ind)
        end = time.time()
        print("Basic find\n---Time consumed in working: ",end - start)

        sorted_tree = create_tree(words)
        start = time.time()
        for ind in range(1000):
            random_word = words[ind]
            binary_tree(sorted_tree, random_word)
        end = time.time()
        print("Sorted binary tree\n---Time consumed in working: ", 10 * (end - start))

        unsorted_tree = create_tree(words)
        random.shuffle(words)
        start = time.time()
        for ind in range(1000):
            random_word = words[ind]
            binary_tree(unsorted_tree, random_word)
        end = time.time()
        print("Shuffle binary tree\n---Time consumed in working: ", 10 * (end - start))

        unsorted_tree.rebalance()
        start = time.time()
        for ind in range(1000):
            random_word = words[ind]
            binary_tree(unsorted_tree, random_word)
        end = time.time()
        print("Balanced binary tree\n---Time consumed in working: ", 10 * (end - start))



my_tree = LinkedBST()
my_tree.demo_bst('words.txt')
