from zipzip_tree import ZipZipTree, Rank, TreeNode
from shell_sort3 import shell_sort3

SCALE = 1e-9
RC = "rc"
BRC = "brc"

def get_brc(node):
	return node.val[BRC] if node else -1.0

# update_brc(): recalculates BRC, from children to param node
def update_brc(node):
	if node is None:
		return
	node.val[BRC] = max(
		node.val[RC],
		get_brc(node.left),
		get_brc(node.right)
	)

# find_first_fit_node(): returns node with tightest fit of current item, rc >= size
# 						 or None if it cannot fit
# note: if None, it should make a new bin? --> Yes!

def find_first_fit_node(node, size):
	# entire subtree cannot fit item!
	if node is None or get_brc(node) < size - SCALE:
		return None 
		
	# check left subtree first
	res = find_first_fit_node(node.left, size)
	if res is not None:
		return res
		
	if node.val[RC] >= size - SCALE:
		return node
		
	else:
		return find_first_fit_node(node.right, size)
	
# fix_brc(): recalculates brc for each node in tree

def fix_brc(node):
	if node is None:
		return
	fix_brc(node.left)
	fix_brc(node.right)
	update_brc(node)

def first_fit(items: list[float], assignment: list[int], free_space: list[float]):
	
	tree = ZipZipTree(capacity=len(items)+1)
	bin_count = 0

	for i, item in enumerate(items):
		print(i, item)
		target = find_first_fit_node(tree.root, item)
		# create new bin
		if target is None:
			print("target is none...")
			free_space.append(1.0)
			rank = tree.get_random_rank()
			
			tree.insert(bin_count, {RC: 1.0, BRC: 1.0}, rank)
			fix_brc(tree.root)
			bin_count += 1
			target = find_first_fit_node(tree.root, item)

		bin_index = target.key
		assignment[i] = bin_index

		old_rc = target.val[RC]
		new_rc = old_rc - item
		free_space[bin_index] = new_rc

		rank = target.rank
		tree.remove(bin_index)
		tree.insert(bin_index, {RC: new_rc, BRC: new_rc}, rank)
		fix_brc(tree.root)

def first_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
	sorted = shell_sort3(items)
	first_fit(sorted, assignment, free_space)

'''
(i, rc, brc)
i: bin index
rc: remaining capacity
brc: best remaining capacity in subtree


				(5, .46, .48)
			/					\
	(3, .32, .45)			(7, .32, .48)
		/		\			/				\
(2, .4, .4)	(4, .45, .45)	(6, .47, .47)	(8, .48, .48)
	/
(1, .3, .3)

item size      | goes to bin
s <= .3        | B1
.3 < s <= .4   | B2
.4 < s <= .45  | B4
.45 < s <= .46 | B5
.46 < s <= .47 | B6
.47 < s <= .48 | B8

'''