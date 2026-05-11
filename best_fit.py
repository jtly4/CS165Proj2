from zipzip_tree import ZipZipTree, Rank, TreeNode
from shell_sort3 import shell_sort3

SCALE = 1e-9
RC = "rc"
BRC = "brc"

# find_best_fit(): returns the node with tightest fit, which is smallest RC >= item_size
# 				   None if no bin fit this item --> start a new bin

def find_best_fit_node(node, item_size):
	if node is None:
		return None
	
	if node.key[0] >= item_size - SCALE:
		left = find_best_fit_node(node.left, item_size)
		return left if left is not None else node
	else:
		return find_best_fit_node(node.right, item_size)


def best_fit(items: list[float], assignment: list[int], free_space: list[float]):
	tree = ZipZipTree(capacity=len(items)+1)
	bin_count = 0

	for i, item in enumerate(items):
		target = find_best_fit_node(tree.root, item)
		

		if target is None:
			#print("target is none")
			# create a new bin
			free_space.append(1.0)
			rank = tree.get_random_rank()

			tree.insert((1.0, bin_count), None, rank)
			bin_count += 1
			target = find_best_fit_node(tree.root, item)

		#print(f"found target: {target.key}")

		bin_index = target.key[1]
		assignment[i] = bin_index

		old_rc = target.key
		new_rc = old_rc[0] - item
		cur_bin = target.key[1]
		rank = target.rank

		free_space[cur_bin] = new_rc
		
		tree.remove(old_rc)
		tree.insert((new_rc, cur_bin), None, rank)

	#print(free_space)

def best_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
	sorted = shell_sort3(items[:])
	best_fit(sorted, assignment, free_space)

'''
0.2, 0.5, 0.4, 0.7, 0.1, 0.3, 0.8

bin1 = 0.2, 0.5, 0.1
bin2 = 0.4
bin3 = 0.7, 0.3

8 7 5 4 3 2 1 


'''