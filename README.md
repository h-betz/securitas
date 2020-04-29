# Securitas

### Getting Started
Version used: python 3.8.1

*Note*: You may want to do the following in a virtual environment

Install requirements: `pip install requirements.txt`


### Merkle Root
##### To run:
cd into the securitas project and open a python terminal.

Import the merkle_tree class `from merkle_tree.merkle_root import MerkleTree`

Create a Merkle Tree instance and pass in your hash function - the hash
function must take a string as its argument and return a string: `tree = MerkleTree(hash_function)`

You can generate the Merkle root of your data by calling the `generate_merkel_root()`
method and passing in your data (as a list) as an argument.

Running tests:

*Note*: The tests, as written may fail depending on your OS, version of python, and
or the version of the hashlib function you currently have installed

cd into the securitas project and open a python terminal.

Enter the following command: `pytest merkle_tree/tests/test_merkle_root.py`

### Crawler
##### To run:
cd into the securitas project and open a python terminal.

Import the crawler class `from crawler.crawler import Crawler`

Create a crawler object instance: `crawler = Crawler()`

You can start the web crawling session by calling the `crawl()` method and passing in 
a url (required) and any of the following arguments:
- clear: Clears the existing output directory
- count: Number of links to scrape
- unique: Boolean determines whether or not the crawler will scrape repeated links
- headers: a dict object containing headers that will be applied to the session
