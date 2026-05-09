'''
# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file

from __future__ import annotations

import math
from typing import TypeVar
from dataclasses import dataclass
import random

# any variable annotated with KeyType should use the same type for each tree, and should be comparable.

# ValType is for any additional data to be stored in the nodes.

# Rank is a container representing each node's rank, both geometric and uniform.
#           If using an earlier form of Python, you can use a named tuple instead.
KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

@dataclass(frozen=True, order=True)
class Rank:
	geometric_rank: int
	uniform_rank: int

class TreeNode:
    def __init__(self, key: KeyType, val: ValType, rank: Rank = None, left=None, right=None):
        self.key = key
        self.val = val
        self.rank = rank
        self.left = left
        self.right = right

class ZipZipTree:
	# ZipZipTree(): constructs the zip-zip tree with a specific capacity.
	def __init__(self, capacity: int):
		self.capacity = capacity
		self.size = 0
		self.root = None
		
	# get_random_rank(): returns a random node rank, chosen independently from:
	#           a geometric distribution of mean 1 and,
	#           a uniform distribution of integers from 0 to log(capacity)^3 - 1 (log capacity cubed minus 1).


	def get_random_rank(self) -> Rank:
		geo_rank = 0
		rand = random.random()

		while rand < 0.5:
			geo_rank += 1
			rand = random.random()

		uni_rank = random.randint(0, int(math.log2(self.capacity) ** 3) - 1)
		return Rank(geometric_rank=geo_rank, uniform_rank=uni_rank)

	# insert(): inserts item with parameter key, value, and rank into tree.
	#           if rank is not provided, a random rank should be selected by using get_random_rank().


	def insert(self, key: KeyType, val: ValType, rank: Rank = None):
		if self.size == self.capacity:
			return "Cannot insert. Max will be exceeded"
		
		self.size += 1

		if not rank:
			rank = get_random_rank()

		node = TreeNode(key, val, rank)

		if not self.root:
			self.root = node
			node.left = None
			node.right = None
			return

		cur = self.root

		while cur and (rank < cur.rank or (rank == cur.rank and key > cur.key)):
			
			if rank > cur.rank:
				break
			elif rank <= cur.rank:
				prev = cur
				cur = cur.left if key < cur.key else cur.right
			
			prev = cur
			cur = cur.left if key < cur.key else cur.right
			

		if cur == self.root:
			if cur.key < key:
				node.left = cur
			elif cur.key >= key:
				node.right = cur
			self.root = node
			return
		elif key < prev.key:
			prev.left = node
		else:
			prev.right = node
		
		prev = node 
		
		while cur:
			fix = prev
			if cur.key < key:
				while cur and cur.key < key:
					prev = cur
					cur = cur.right
					is_right = True
			else:
				while cur and cur.key > key:
					prev = cur
					cur = cur.left
					is_right = False
			
			this doesn't make sense to me because we set fix <- prev <- node...
			if fix.key > key or (fix == node and prev.key > key):
				fix.left = cur
			
			if prev.key > key:
				fix.left = cur
			else:
				fix.right = cur

			if is_right:
				prev.right = None
			else:
				prev.left = None

		return
	
	# search(): returns the node being searched 
	def search(self, key: KeyType):
		cur = self.root
		while cur.key != key: 
			prev = cur
			if cur.key > key:
				cur = cur.left
			elif cur.key < key:
				cur = cur.right
			else:
				break

		return [cur, prev]

	# remove(): removes item with parameter key from tree.
	#           you can assume that the item exists in the tree.

	def remove(self, key: KeyType):
		nodes = self.search(key)
		node = nodes[0]
		prev = nodes[1]
		
		if node: 
			self.size -= 1

		if node.left:
			left = node.left

		if node.right:
			right = node.right
		

		cur = self.root
		while cur.key != key:
			prev = cur
			cur = cur.left if key < cur.key else cur.right

		left = cur.left
		right = cur.right

		if not left:
			cur = right
		elif not right: 
			cur = left
		elif left.rank >= right.rank:
			cur = left
		else:
			cur = right

		if key == self.root.key:
			self.root = cur
		elif key < prev.key:
			prev.left = cur
		else:
			prev.right = cur

		while left and right:
			if left.rank >= right.rank:
				while left or left.rank < right.rank:
					prev = left
					left = left.right
				prev.right = right
			else:
				while right or left.rank >= right.rank:
					prev = right
					right = right.left
				prev.left = left 

		self.size -= 1

		return


	# find(): returns the value of item with parameter key.
	#         you can assume that the item exists in the tree.

	def find(self, key: KeyType) -> ValType:
		if not self.root:
			return None
		
		cur = self.root

		while cur:
			if cur.key < key:
				cur = cur.right
			elif cur.key > key:
				cur = cur.left
			else:
				break

		return cur.val

		

	# get_size(): returns the number of nodes in the tree.

	def get_size(self) -> int:
		return self.size
		

	# get_height(): returns the height of the tree.

	def get_height(self) -> int:
		if not self.root:
			return -1
		
		def calc_height(node: TreeNode):
			if not node:
				return -1
			return 1 + max(calc_height(node.left), calc_height(node.right))
		
		return calc_height(self.root)


	# get_depth(): returns the depth of the item with parameter key.
	#              you can assume that the item exists in the tree.

	def get_depth(self, key: KeyType):
		depth = 0

		if not self.root:
			return 0

		cur = self.root
		
		while cur:
			depth += 1
			if cur.key > key:
				cur = cur.left
			elif cur.key < key:
				cur = cur.right
			else:
				break

		return depth

		

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define
'''

# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file

from __future__ import annotations

import math
from typing import TypeVar
from dataclasses import dataclass
import random

# any variable annotated with KeyType should use the same type for each tree, and should be comparable.

# ValType is for any additional data to be stored in the nodes.

# Rank is a container representing each node's rank, both geometric and uniform.
#           If using an earlier form of Python, you can use a named tuple instead.
KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

@dataclass(frozen=True, order=True)
class Rank:
	geometric_rank: int
	uniform_rank: int

class TreeNode:
    def __init__(self, key: KeyType, val: ValType, rank: Rank = None, left=None, right=None):
        self.key = key
        self.val = val
        self.rank = rank
        self.left = left
        self.right = right

class ZipZipTree:
	# ZipZipTree(): constructs the zip-zip tree with a specific capacity.
	def __init__(self, capacity: int):
		self.capacity = capacity
		self.size = 0
		self.root = None
		
	# get_random_rank(): returns a random node rank, chosen independently from:
	#           a geometric distribution of mean 1 and,
	#           a uniform distribution of integers from 0 to log(capacity)^3 - 1 (log capacity cubed minus 1).


	def get_random_rank(self) -> Rank:
		geo_rank = 0
		rand = random.random()

		while rand < 0.5:
			geo_rank += 1
			rand = random.random()

		uni_rank = random.randint(0, int(math.log2(self.capacity) ** 3) - 1)
		return Rank(geometric_rank=geo_rank, uniform_rank=uni_rank)

	# insert(): inserts item with parameter key, value, and rank into tree.
	#           if rank is not provided, a random rank should be selected by using get_random_rank().


	def insert(self, key: KeyType, val: ValType, rank: Rank = None):
		#if self.size == self.capacity:
		#	return "Cannot insert. Max will be exceeded"
		
		#print(f"Inserting: {key}, {val}, {rank.uniform_rank}, {rank.geometric_rank} !!")
		
		self.size += 1

		if not rank:
			rank = get_random_rank()

		node = TreeNode(key, val, rank)

		if not self.root:
			#print("Starting fresh tree! This is the root.")
			self.root = node
			return

		cur = self.root

		while cur and (rank < cur.rank or (rank == cur.rank and key > cur.key)):
			#print(f"Current node: {cur.key}, {cur.val}, {cur.rank}")
			if rank > cur.rank:
				#print(f"New node rank {rank} > {cur.rank}")
				#print("We stop here")
				break
			elif rank <= cur.rank:
				prev = cur
				#cur = cur.left if key < cur.key else cur.right
				if key < cur.key:
					cur = cur.left
					#print("Traversing left")
				else:
					cur = cur.right
					#print("Traversing right")

		if cur == self.root:
			#print("We are at root. Moving old root to the new  root's...")
			if cur.key < key:
				node.left = cur
				#print("left")
			elif cur.key >= key:
				node.right = cur
				#print("right")
			self.root = node
			return
		elif key < prev.key:
			#print(f"key: {key} < prev key: {prev.key}")
			#print(f"new node will be left of ({prev.key}, {prev.val})")
			prev.left = node
		else:
			#print(f"key: {key} >= prev key: {prev.key}")
			#print(f"new node will be right of ({prev.key}, {prev.val})")
			prev.right = node

		if not cur:
			#print(f"New node will be a child of {prev.key}, {prev.val}")
			node.left = None
			node.right = None
			#print("Insertion complete")
			return
		else:
			#print("The current node will be the new node's...")
			if key < cur.key:
				node.right = cur 
				#print("right")
			else:
				node.left = cur 
				#print("left")

		prev = node 
		#print("Finding replacement")
		while cur:
			fix = prev
			if cur.key < key:
				#print("going right")
				while cur and cur.key < key:
					prev = cur
					cur = cur.right
					is_right = True
			else:
				#print("going left")
				while cur and cur.key > key:
					prev = cur
					cur = cur.left
					is_right = False
			
			# this doesn't make sense to me because we set fix <- prev <- node...
			if fix.key > key or (fix == node and prev.key > key):
				fix.left = cur
			else:
				fix.right = cur
			'''
			if prev.key > key:
				fix.left = cur
			else:
				fix.right = cur

			if is_right:
				prev.right = None
			else:
				prev.left = None
			'''

		return
	
	# search(): returns the node being searched 
	def search(self, key: KeyType):
		cur = self.root
		while cur.key != key: 
			prev = cur
			if cur.key > key:
				cur = cur.left
			elif cur.key < key:
				cur = cur.right
			else:
				break

		return [cur, prev]

	# remove(): removes item with parameter key from tree.
	#           you can assume that the item exists in the tree.

	def remove(self, key: KeyType):
		'''nodes = self.search(key)
		node = nodes[0]
		prev = nodes[1]
		
		if node: 
			self.size -= 1

		if node.left:
			left = node.left

		if node.right:
			right = node.right
		'''

		cur = self.root
		while cur.key != key:
			prev = cur
			cur = cur.left if key < cur.key else cur.right

		left = cur.left
		right = cur.right

		if not left:
			cur = right
		elif not right: 
			cur = left
		elif left.rank >= right.rank:
			cur = left
		else:
			cur = right

		if key == self.root.key:
			self.root = cur
		elif key < prev.key:
			prev.left = cur
		else:
			prev.right = cur

		while left and right:
			if left.rank >= right.rank:
				while left and left.rank >= right.rank:
					prev = left
					left = left.right
				prev.right = right
			else:
				while right and left.rank < right.rank:
					prev = right
					right = right.left
				prev.left = left 

		self.size -= 1

		return


	# find(): returns the value of item with parameter key.
	#         you can assume that the item exists in the tree.

	def find(self, key: KeyType) -> ValType:
		if not self.root:
			return None
		
		cur = self.root

		while cur:
			if cur.key < key:
				cur = cur.right
			elif cur.key > key:
				cur = cur.left
			else:
				break

		return cur.val

		

	# get_size(): returns the number of nodes in the tree.

	def get_size(self) -> int:
		return self.size
		

	# get_height(): returns the height of the tree.

	def get_height(self) -> int:
		if not self.root:
			return -1
		
		def calc_height(node: TreeNode):
			if not node:
				return -1
			return 1 + max(calc_height(node.left), calc_height(node.right))
		
		return calc_height(self.root)


	# get_depth(): returns the depth of the item with parameter key.
	#              you can assume that the item exists in the tree.

	def get_depth(self, key: KeyType):
		depth = 0

		cur = self.root

		while cur.key != key:
			depth += 1
			if cur.key > key:
				cur = cur.left
			else:
				cur = cur.right

		return depth

'''
[InsertType(4, 'a', requirements.Rank(0, 9)), InsertType(5, 'b', requirements.Rank(0, 9)), InsertType(2, 'c', requirements.Rank(1, 12)), InsertType(1, 'd', requirements.Rank(1, 5))]

		2, c, 1, 12
		/		\
1, d, 1, 5  	4, a, 0, 9
    /      			\
0, e, 1, 5		  	5, b, 0, 9


data2 = [InsertType(4, 'a', requirements.Rank(2, 1)), InsertType(5, 'b', requirements.Rank(2, 2)), InsertType(2, 'c', requirements.Rank(1, 8)), InsertType(1, 'd', requirements.Rank(0, 12)), InsertType(0, 'e', requirements.Rank(1, 8))]

			5, b, 2, 2
			/
		4, a, 2, 1
		/			\
	2, c, 1, 8	 	5, b, 2, 2
	/
0, e, 1, 8
 /
1, d, 0, 12


'''