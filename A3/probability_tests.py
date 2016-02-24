"""Contains various tests for Assignment 3."""

def network_setup_test(power_plant):
	"""Test that the power plant 
	network has the proper number
	of nodes and edges."""
	nodes = power_plant.nodes
	if(len(nodes)==5):
		print('correct number of nodes')
		total_links = sum([len(n.children) for n in nodes] + [len(n.parents) for n in nodes])
		if(total_links == 10):
			print('correct number of edges between nodes')
		else:
			print('incorrect number of edges between nodes')
	else:
		print('incorrect number of nodes')

def probability_setup_test(power_plant):
	"""Test that all nodes in the 
	power plant network have proper
	probability distributions.
	Note that all nodes have to be
	named predictably for tests to
	run correctly."""
	
	# first test temperature distribution
	T_node = power_plant.get_node_by_name('temperature')
	if(T_node is not None):
		T_dist = T_node.dist.table
		if(len(T_dist) == 2):
			print('correct temperature distribution size')
			test_prob = T_dist[0]
			if(int(test_prob*100) == 80):
				print('correct temperature distribution')
		else:
			print('incorrect temperature distribution size')

	# then faulty gauge distribution
	F_G_node = power_plant.get_node_by_name('faulty gauge')
	if(F_G_node is not None):
		F_G_dist = F_G_node.dist.table
		rows, cols = F_G_dist.shape
		if(rows == 2 and cols == 2):
			print('correct faulty gauge distribution size')
			test_prob1 = F_G_dist[0][1]
			test_prob2 = F_G_dist[1][0]
			if(int(test_prob1*100) == 5 and int(test_prob2*100) == 20):
				print('correct faulty gauge distribution')
			else:
				print('incorrect faulty gauge distribution')
		else:
			print('incorrect faulty gauge distribution size')

	# gauge distribution
	# can't test exact probabilities because
	# order of probabilties is not guaranteed
	G_node = power_plant.get_node_by_name('gauge')
	if(G_node is not None):
		G_dist = G_node.dist.table
		rows1, rows2, cols = G_dist.shape
		if(rows1 == 2 and rows2 == 2 and cols == 2):
			print('correct gauge distribution size')
		else:
			print('incorrect gauge distribution size')

	# alarm distribution
	A_node = power_plant.get_node_by_name('alarm')
	if(A_node is not None):
		A_dist = A_node.dist.table	
		rows1, rows2, cols = A_dist.shape
		if(rows1 == 2 and rows2 == 2 and cols == 2):
			print('correct alarm distribution size')
		else:
			print('incorrect alarm distribution size')

	# faulty alarm distribution
	F_A_node = power_plant.get_node_by_name('faulty alarm')
	if(F_A_node is not None):
		F_A_dist = F_A_node.dist.table
		if(len(F_A_dist) == 2):
			print('correct faulty alarm distribution size')
			test_prob = F_A_dist[0]
			if(int(test_prob*100) == 85):
				print('correct faulty alarm distribution')
		else:
			print('incorrect faulty alarm distribution size')
