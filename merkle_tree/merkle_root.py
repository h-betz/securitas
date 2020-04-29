import math

class MerkleTreeNode:

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class MerkleTree:

    def __init__(self, hash_function):
        self.hash_function = hash_function

    def _hash_data(self, data):
        """
        Calls the hash function on the data string being passed in
        :param data: str
        :return: str
        """
        return self.hash_function(data)

    def _hash_data_list(self, data_list):
        """
        Hashes each of the data blocks in a list
        :param data_list: List of strings
        :return: List of hashed strings
        """
        return [self._hash_data(data) for data in data_list]

    def _build_leaf_nodes(self, leaves):
        """
        Create the bottom layer of MerkleTreeNodes
        :param leaves:
        :return:
        """
        leaf_nodes = [MerkleTreeNode(leaf) for leaf in leaves]
        return leaf_nodes

    def _build_level(self, children):
        """
        Builds a parent level of MerkleTreeNodes from a list of child nodes
        :param children: List of MerkleTreeNodes
        :return: List of MerkleTreeNodes
        """
        level = []
        n = len(children)
        for i in range(1, n, 2):
            left = children[i - 1]
            right = children[i]
            data = self._hash_data(left.value + right.value)
            node = MerkleTreeNode(data, left=left, right=right)
            level.append(node)

        if n % 2 != 0:
            # Handling for the cases where the number of children is odd
            level.append(children.pop())

        return level

    def _build_tree(self, children):
        """
        Build the Merkle Tree from the leaf nodes up
        :param children: A list of MerkleTreeNodes
        :return: str
        """
        n = math.ceil(math.log(len(children), 2))
        while n > 0:
            children = self._build_level(children)
            n -= 1

        return children[0]

    def generate_merkel_root(self, data_list):
        """
        Given a list of data, return the Merkle root
        :param data_list: List of data
        :return: str
        """
        if not data_list:
            return None

        encoded_data = self._hash_data_list(data_list)
        leaves = self._build_leaf_nodes(encoded_data)
        return self._build_tree(leaves).value
