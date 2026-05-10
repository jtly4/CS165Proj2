from zipzip_tree import ZipZipTree, Rank, TreeNode

def first_fit(items: list[float], assignment: list[int], free_space: list[float]):
	SCALE = 1e-9
	tree = ZipZipTree(capacity=len(items)+1)
	bin_count = 0

	
	def get_brc(node):
		return node.val['brc'] if node else -1.0
	
	# update_brc(): recalculates BRC, from children to param node
	def update_brc(node):
		if node is None:
			return
		node.val['brc'] = max(
			node.val['rc'],
			get_brc(node.left),
			get_brc(node.right)
		)

	# find_first_fit_node(): returns node with tightest fit of current item, rc >= size
	# 						 or None if it cannot fit
	# note: if None, it should make a new bin? 

	def find_first_fit_node(node, size):
		# entire subtree cannot fit item!
		if node is None or get_brc(node) < size - SCALE:
			return None 
		
		# check left subtree first
		res = find_first_fit_node(node.left, size)
		if res is not None:
			return res
		
		if node.val['rc'] >= size - SCALE:
			return node
		
		else:
			return find_first_fit_node(node.right, size)











































def first_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
	pass

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