from __future__ import division
from osm2networkx import *
import random
import pickle
import time

class InsertionSortQueue():
    
    def __init__(self):
        self.queue = []

    def next(self):
        self.queue.pop()

    def __str__(self):
        return 'ISQ:[%s]'%(', ').join([str(i) for i in self.queue])

    def append(self, node):

        self.queue.append(node)
        self.queue = sorted(self.queue)

        def __eq__(self, other):
            return self == other

        def clear(self):
            del(self.queue[:])

        __next__ = next

def is_path_correct(graph, start, goal, path ):
    if start == goal:
        return not path

    if not path[0]==start and path[-1] == goal:
        return False
    
    for i in range(0, len(path)-1):
        edges = networkx.edges(graph, path[i])
        if not any([path[i+1] == v for e,v in edges] ):
            return False

    return True

def is_path_cost_correct(graph, path, cost):
    if not path and not cost:
        return True

    if not path and cost:
        return False
    
    correct_cost = 0
    for i in range(0, len(path)-1):
        edge_weight = graph.get_edge_data(path[i], path[i+1])['weight']
        correct_cost += edge_weight

    return cost == correct_cost

def get_path_cost(graph, path):

    if not path:
        return 0

    cost = 0
    
    for i in range(0, len(path) -1):
        if not graph.get_edge_data(path[i], path[i+1]):
            print path[i], path[i+1]
            print networkx.edges(graph, path[i])
            print networkx.edges(graph, path[i+1])
        edge_weight = graph.get_edge_data(path[i], path[i+1])['weight']
        cost += edge_weight

    return cost



def bfs_tests(breadth_first_search):
    
    romania = pickle.load(open('romania_graph.pickle', 'rb'))

    bfs_paths = pickle.load(open('romania_test_paths.pickle', 'rb' ))

    for key, value in bfs_paths.items():
        start, goal = key

        right_path, right_closed = value
        
        path, closed = breadth_first_search(romania, start, goal)

        path_is_valid = is_path_correct(romania, start, goal, path)
        
        max_nodes_explored = max(len(right_closed)*3, len(right_closed) + 3)
        node_exploration_valid = len(closed) <= max_nodes_explored
        
        path_is_correct = True

        if path:
            path_is_correct = len(path) <= len(right_path)

        if not (path_is_valid and node_exploration_valid and path_is_correct):
            print('Breadth first search fails benchmarks searching from %s to %s: '%(start, goal))
            
            if not path_is_valid:
                print('Path %s does not go from %s to %s'%(str(path),str(start), str(goal)))
        
            if not node_exploration_valid:
                print('Nodes explored should be a valid frontier, and be no more than %d in number'%(max_nodes_explored))

            if not path_is_correct:
                print('Path %s is longer than an optimal path %s'%(str(path),str(right_path)))
            return 
    print('BFS tests passed.')


def priority_queue_tests(PriorityQueue, ReferenceQueue=InsertionSortQueue):

    order_check_pq = PriorityQueue()
    temp_list = []

    for i in range(10000):
        a = random.randint(0,10000)
        order_check_pq.append(a)
        temp_list.append(a)

    temp_list = sorted(temp_list)

    for i in temp_list:
        j = order_check_pq.pop()
        if not i == j:
            print('Priority queue ordering incorrect:')
            return

    pq = PriorityQueue()

    reference_times_list = []
    reference_pq = ReferenceQueue()
    for i in range(10000):
        reference_start_time = time.time()
        reference_pq.append(random.randint(0,10000))
        reference_end_time = time.time()
        
        reference_times_list.append(reference_end_time - reference_start_time)

    pq_insertion_times = []

    for i in range(10000):
        
        pq_start_time = time.time()
        pq.append(('a', random.randint(0,10000)))
        pq_end_time = time.time()
        
        pq_insertion_times.append(pq_end_time - pq_start_time)
    
    #average times should not exceed those of list by more than 10%.

    average_list_insert = sum(reference_times_list)/len(reference_times_list)
    average_pq_insert = sum( pq_insertion_times )/ len( pq_insertion_times )


    if average_pq_insert > average_list_insert:
        print('Priority queue insertion should be amortized O(1),\
        but performance significantly differs from that of a list.')
        print('Average insertion time for PQ: %f'%average_pq_insert)
        print('Average insertion time for list: %f'%average_list_insert)
        return
    print('PriorityQueue tests passed')

def ucs_tests(uniform_cost_search):

    romania = pickle.load(open('romania_graph.pickle', 'rb'))

    ucs_paths = pickle.load(open('romania_ucs_test_paths.pickle', 'rb' ))

    for key, value in ucs_paths.items():
        start, goal = key

        right_path, right_closed, right_cost = value
        
        path, closed, cost = uniform_cost_search(romania, start, goal)

        path_is_valid = is_path_correct(romania, start, goal, path)
        
        max_path_length = max(len(right_closed)*2, len(right_closed) + 3)
        node_exploration_valid = len(closed) <= max_path_length
        
        path_is_correct = True

        if path:
            path_is_correct = cost <= right_cost

        if not (path_is_valid and node_exploration_valid and path_is_correct):
            print('Uniform cost search fails benchmarks searching from %s to %s: '%(start, goal))
            
            if not path_is_valid:
                print('Path %s does not go from %s to %s'%(str(path),str(start), str(goal)))
        
            if not node_exploration_valid:
                print('Nodes explored should be a valid frontier, and be no more than %d in number'%(max_path_length))

            if not path_is_correct:
                print('Path %s is longer than an optimal path %s'%(str(path),str(right_path)))

            if not cost == right_cost:
                print('Path cost is incorrect. Given as %d, should be %d'%(cost, right_cost))

            return 

    print 'Uniform cost search tests passed'

def a_star_tests(a_star, null_heuristic, euclidean_distance):

    romania = pickle.load(open('romania_graph.pickle', 'rb'))

    a_star_paths = pickle.load(open('romania_null_a_star_test_paths.pickle', 'rb' ))

    for key, value in a_star_paths.items():

        start, goal = key

        right_path, right_closed = value
        
        path, closed = a_star(romania, start, goal, null_heuristic)

        path_is_valid = is_path_correct(romania, start, goal, path)
        
        max_nodes_explored = max(len(right_closed)*2, len(right_closed) + 3)
        node_exploration_valid = len(closed) <= max_nodes_explored
        
        path_is_correct = True


        if right_path:

            correct_cost = 0
            
            for i in range(0, len(path)-1):
                edge_weight = romania.get_edge_data(right_path[i], right_path[i+1])['weight']
                correct_cost += edge_weight
            
            path_is_correct = is_path_cost_correct(romania, path, correct_cost)

        if not (path_is_valid and node_exploration_valid and path_is_correct):
            print('A star search fails benchmarks searching from %s to %s: '%(start, goal))
            
            if not path_is_valid:
                print('Path %s does not go from %s to %s'%(str(path),str(start), str(goal)))
        
            if not node_exploration_valid:
                print('Nodes explored should be a valid frontier, and be no more than %d in number'%(len(closed)*1.1))

            if not path_is_correct:
                print('Path %s is longer than an optimal path %s'%(str(path),str(right_path)))

            return 

    print('A star null_heuristic search tests passed')
    
    euclidean_paths = pickle.load( open( 'romania_euclidean_a_star_test_paths.pickle' , 'rb')  )

    for key, value in euclidean_paths.items():

        start, goal = key

        right_path, right_closed = value
        
        path, closed = a_star(romania, start, goal, euclidean_distance)

        path_is_valid = is_path_correct(romania, start, goal, path)
        
        max_nodes_explored = max(len(right_closed)*1.1, len(right_closed) + 3)
        node_exploration_valid = len(closed) <= max_nodes_explored
        
        path_is_correct = True


        if right_path:

            correct_cost = 0
            
            for i in range(0, len(path)-1):
                edge_weight = romania.get_edge_data(right_path[i], right_path[i+1])['weight']
                correct_cost += edge_weight
            
            path_is_correct = is_path_cost_correct(romania, path, correct_cost)

        if not (path_is_valid and node_exploration_valid and path_is_correct):
            print('A star search fails benchmarks searching from %s to %s: '%(start, goal))
            
            if not path_is_valid:
                print('Path %s does not go from %s to %s'%(str(path),str(start), str(goal)))
        
            if not node_exploration_valid:
                print('Nodes explored should be a valid frontier, and be no more than %d in number'%(max_nodes_explored))

            if not path_is_correct:
                print('Path %s is longer than an optimal path %s'%(str(path),str(right_path)))

            return 

    print('A star euclidean_dist_heuristic search tests passed')

def bidirectional_tests(bidirectional_ucs):

    romania = pickle.load(open('romania_graph.pickle', 'rb'))

    ucs_paths = pickle.load(open('romania_ucs_bidirectional_test_paths.pickle', 'rb' ))

    for key, value in ucs_paths.items():
        start, goal = key

        right_path, right_closed = value
        right_start_closed, right_goal_closed = right_closed

        path, closed = bidirectional_ucs(romania, start, goal)
        
        start_closed, goal_closed = closed

        path_is_valid = is_path_correct(romania, start, goal, path)
        
        max_nodes_explored_start = max(len(right_start_closed)*2, len(right_start_closed) + 3)
        max_nodes_explored_goal = max(len(right_goal_closed)*2, len(right_goal_closed) + 3)
        node_exploration_valid = (len(start_closed) <= max_nodes_explored_start and 
                                    len(goal_closed) <= max_nodes_explored_goal)
        
        path_is_correct = True

        if path and right_path:
            print right_path
            path_is_correct = get_path_cost(romania, path) <= get_path_cost(romania, right_path)

        if not (path_is_valid and node_exploration_valid and path_is_correct):
            print('Uniform cost search fails benchmarks searching from %s to %s: '%(start, goal))
            
            if not path_is_valid:
                print('Path %s does not go from %s to %s'%(str(path),str(start), str(goal)))
        
            if not node_exploration_valid:
                print('Explored more nodes than necessary, start_closed should be no more than %d in number and goal_closed should be no more than %d in number'%
                    (max_nodes_explored_start , max_nodes_explored_goal))

            if not path_is_correct:
                print('Path %s is longer than an optimal path %s'%(str(path),str(right_path)))

            return 

    print('Bidirectional uniform cost search tests passed')


