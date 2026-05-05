# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file

from __future__ import annotations

from typing import TypeVar
from dataclasses import dataclass

# any variable annotated with KeyType should use the same type for each tree, and should be comparable.

# ValType is for any additional data to be stored in the nodes.

# Rank is a container representing each node's rank, both geometric and uniform.
#           If using an earlier form of Python, you can use a named tuple instead.
KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

@dataclass
class Rank:
	geometric_rank: int
	uniform_rank: int

class ZipZipTree:
	# ZipZipTree(): constructs the zip-zip tree with a specific capacity.
	def __init__(self, capacity: int):
		capacity = capacity
		
	# get_random_rank(): returns a random node rank, chosen independently from:
	#           a geometric distribution of mean 1 and,
	#           a uniform distribution of integers from 0 to log(capacity)^3 - 1 (log capacity cubed minus 1).


	def get_random_rank(self) -> Rank:
		pass

	# insert(): inserts item with parameter key, value, and rank into tree.
	#           if rank is not provided, a random rank should be selected by using get_random_rank().


	def insert(self, key: KeyType, val: ValType, rank: Rank = None):
		pass

	# remove(): removes item with parameter key from tree.
	#           you can assume that the item exists in the tree.


	def remove(self, key: KeyType):
		pass

	# find(): returns the value of item with parameter key.
	#         you can assume that the item exists in the tree.

	def find(self, key: KeyType) -> ValType:
		pass

	# get_size(): returns the number of nodes in the tree.

	def get_size(self) -> int:
		pass

	# get_height(): returns the height of the tree.

	def get_height(self) -> int:
		pass

	# get_depth(): returns the depth of the item with parameter key.
	#              you can assume that the item exists in the tree.

	def get_depth(self, key: KeyType):
		pass

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define
