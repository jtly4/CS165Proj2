# Example file: next_fit.py

# params:
# 	items: the items to assign to the bins
# 	assignment: the assignment of the ith item to the jth bin for all i items.
# 	            bin numbers start from 0.
# 	            assume len(assignment) == len(items).
# 	            you should not add any new elements to this list.
# 	            you must modify this list's elements to indicate the assignment.
# 	            see comment below for first-fit decreasing and for best-fit decreasing.
#
# 	free_space: the amount of space left in the jth bin for all j bins created by the algorithm.
# 	            you should add one element for each bin that the algorithm creates.
# 	            when the function returns, this should indicate the final free space available in each bin.

'''
def next_fit(items: list[float], assignment: list[int], free_space: list[float]):
	SCALE = 1e-10
	bin_count = 0
	cur_capacity = 0
	remaining_capacity = SCALE

	bins = {bin_count: []}
	for i, item in enumerate(items):
		rounded = item*SCALE
		if cur_capacity >= SCALE or (cur_capacity + rounded > SCALE):
			free_space.append(remaining_capacity / SCALE)
			bin_count += 1
			bins[bin_count] = []
			cur_capacity = 0
			remaining_capacity = SCALE


		bins[bin_count].append(item)
		cur_capacity += rounded
		remaining_capacity -= rounded
		assignment[i] = bin_count
		print(cur_capacity, remaining_capacity)

	# need to handle last element if it didn't fill up current bin 
	if len(free_space) != bin_count:
		free_space.append(remaining_capacity / SCALE)

	return free_space
'''

def next_fit(items: list[float], assignment: list[int], free_space: list[float]):
	bin_count = 0
	cur_capacity = 0
	remaining_capacity = 1.0

	bins = {bin_count: []}
	for i in range(len(items)):
		if cur_capacity >= 1 or (cur_capacity + items[i] >= 1):
			# free_space[bin_count] = remaining_capacity
			free_space.append(remaining_capacity)
			bin_count += 1
			bins[bin_count] = []
			cur_capacity = 0
			remaining_capacity = 1.0


		bins[bin_count].append(items[i])
		cur_capacity += items[i]
		remaining_capacity -= items[i]
		assignment[i] = bin_count

	# need to handle last element if it didn't fill up current bin 
	if len(free_space) != bin_count:
		free_space.append(remaining_capacity)

	return free_space


items = [0.7, 0.5, 0.2, 0.1, 0.2, 0.9, 0.3]
items = [0.79, 0.88, 0.95, 0.12, 0.05, 0.46, 0.53, 0.64, 0.04, 0.38, 0.03, 0.26]

# assignment = [0, 1, 2, 3, 4, 5, 6]
assignment = [0] * len(items)
free_space = []

# print(next_fit(items, assignment, free_space))