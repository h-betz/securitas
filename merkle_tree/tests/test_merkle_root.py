import hashlib
from merkle_tree.merkle_root import MerkleTree

def test__merkle_root_SHA256():

    def my_sha256(data):
        return hashlib.sha256(str.encode(data)).hexdigest()

    data_list = ['a', 'string', 'to', 'test', 'my', 'sha256 function']
    tree = MerkleTree(my_sha256)
    root = tree.generate_merkel_root(data_list)
    assert root == '4510f239ee2d9adc05da5b4160ec9b6dc8b869178bb7c38c51bcd024eb7022f6'

def test__merkle_root_SHA1():

    def my_sha1(data):
        return hashlib.sha1(str.encode(data)).hexdigest()

    data_list = ['astringtotestmysha256function'] * 8
    tree = MerkleTree(my_sha1)
    root = tree.generate_merkel_root(data_list)
    assert root == '30bc55e9721de3966f1bf1c0317219cb8312fab8'

def test__merkle_root_SHA224():

    def my_sha224(data):
        return hashlib.sha224(str.encode(data)).hexdigest()

    data_list = ['the', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy']
    tree = MerkleTree(my_sha224)
    root = tree.generate_merkel_root(data_list)
    assert root == '2719a708014596cbcefe7bb228ec8cb4dee95103970f8559f5b9fc02'

def test__merkle_root_SHA384():

    def my_sha384(data):
        return hashlib.sha384(str.encode(data)).hexdigest()

    data_list = ['star wars'] * 500
    tree = MerkleTree(my_sha384)
    root = tree.generate_merkel_root(data_list)
    assert root == 'c03798bef9ca6e009212052ea2246ebae7f39d9fae3e9f907106a97aa82ca8ec755db859b1305b877f88d3b1d5c4a1af'

def test__merkle_root_SHA512():

    def my_sha512(data):
        return hashlib.sha512(str.encode(data)).hexdigest()

    data_list = ['securitas'] * 1000
    tree = MerkleTree(my_sha512)
    root = tree.generate_merkel_root(data_list)
    assert root == '920e8b99bea95dfec92cbd129de3ae926c2e7c7e6d9363b965cceab01c8c924f888c0a59d38c3dc31339051dd5c096d3a9550a6bbd957b363b496b92303d54ef'