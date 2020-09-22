# CS561 HW1 3D maze
# Zhiqin Lei
# USCID: 1436737564

# input a 3D maze and use three methods to find the optimal path and output it

import math
import collections
import time
from collections import defaultdict
from collections import namedtuple
from collections import deque
from queue import Queue
from queue import PriorityQueue


# read input file
start_time = time.time() # record the time cost 
f = open("input.txt", 'r+')
search_method = f.readline().rstrip('\n') #first line: search method
maze = [int(i) for i in f.readline().rstrip('\n').split(' ')] #second line: size of x,y,z 
start = [int(i) for i in f.readline().rstrip('\n').split(' ')] #third line: entrance grid location
end = [int(i) for i in f.readline().rstrip('\n').split(' ')] #fourth line: exit grid location
num = int(f.readline().rstrip('\n')) #fifthe line: num of grids in maze

grids_list = [] #list of grids and actions eg: [[1, 3, 1, 5], [1, 3, 2, 1, 11]]

for n in range(num): #add follwing n lines into grdis_list
    grids_list.append([int(i) for i in f.readline().rstrip('\n').split(' ')]) 
    

#define an act function
def act(g, a): # input grid and action, output next grid and cost

    if 1 <= a & a <= 6:     # go side, each step cost 10
        c = 10
    elif 7<= a & a <= 18:   # go diagonal, each step cost 14
        c = 14
    if a == 1:
        g[0] += 1
    elif a == 2:
        g[0] -= 1
    elif a == 3:
        g[1] += 1
    elif a == 4:
        g[1] -= 1
    elif a == 5:
        g[2] += 1
    elif a == 6:
        g[2] -= 1
    elif a == 7:
        g[0] += 1
        g[1] += 1
    elif a == 8:
        g[0] += 1
        g[1] -= 1
    elif a == 9:
        g[0] -= 1
        g[1] += 1
    elif a == 10:
        g[0] -= 1
        g[1] -= 1
    elif a == 11:
        g[0] += 1
        g[2] += 1
    elif a == 12:
        g[0] += 1
        g[2] -= 1
    elif a == 13:
        g[0] -= 1
        g[2] += 1
    elif a == 14:
        g[0] -= 1
        g[2] -= 1
    elif a == 15:
        g[1] += 1
        g[2] += 1
    elif a == 16:
        g[1] += 1
        g[2] -= 1
    elif a == 17:
        g[1] -= 1
        g[2] += 1
    elif a == 18:
        g[1] -= 1
        g[2] -= 1
    return g, c

#defin a graph class
class Graph: 
  
    # Constructor 
    def __init__(self): 
  
        # use default dictionary to store adjacent 
        self.adjacent = defaultdict(list) 
        # use dic to store cost
        self.weights = defaultdict(list)
  
    # function to add an edge to graph 
    def addEdge(self,u,v): 
        self.adjacent[u].append(v) 
    
    # function to add weighted cost
    def addCost(self,u,v,c):
        self.adjacent[u].append([v,c])
    
    

# Function to trace the path of search algrithem
def backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path

# Function of BFS method
def BFS(graph, start, end): 
    parent = {}                             # parent records the parent of grid 
    visited = set()                         # record visited grids
    queue = [start]                         # use a queue to find optimal path
    while queue:
        grid = queue.pop(0)                 # pop grid from queue
        if grid not in visited:
            visited.add(grid)               # if not visited before add it to visited
            if grid == end:                 # if find the end, return path
                path = backtrace(parent, start, end)
                return path
            for n in graph.adjacent[grid]:  #check adjacent grids
                if n not in visited:        # if not visited before
                    parent[n] = grid        # record the parent
                    queue.append(n)         # add adjacent to queue
                

# Function of UCS method
def UCS(graph, start, end): # similar to BFS except weighted edge           
    parent = {}
    visited = set()
    queue = PriorityQueue()                 # use priority queue to always pop least cost grid
    queue.put((0, start, [0]))              # put total cost, start grid and cost each step in to queue
    while queue:
        cost, grid, cpath= queue.get()      # use cpath to record every step cost in the path
        if grid not in visited:
            visited.add(grid)
            if grid == end:
                path = backtrace(parent, start, end)
                return path, cost, cpath
            for i in graph.adjacent[grid]:
                if i[0] not in visited:
                    parent[i[0]] = grid
                    new_path = list(cpath)  # use new_path as a temple list of cpath
                    new_path.append(i[-1])  # update step cost and total cost 
                    total_cost = cost + i[-1]
                    queue.put((total_cost, i[0], new_path))

# Heuristic function for calculating future cost
def heuristic(a, b): # find the direct distance from a to b, since each step costs 10, times result 10.             
    (x1, y1, z1) = a
    (x2, y2, z2) = b
    return math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)*10

# Function of A* method
def A(graph, start, end): # similar to BFS except weighted edge           
    parent = {}
    visited = set()
    queue = PriorityQueue()                 # use priority queue to always pop least cost grid
    queue.put((0, start))                   # put total cost, start grid in to queue
    cost = {}
    cost[start] = 0
    cpath = {}
    cpath[start] = 0
    while queue:
        c, grid = queue.get()      
        if grid not in visited:
            visited.add(grid)
            if grid == end:
                path = backtrace(parent, start, end)
                return path, cost[end], cpath
            for i in graph.adjacent[grid]:
                newcost = cost[grid] + i[-1] # use newcost to record actual cost
                if i[0] not in visited :
                    cpath[i[0]] = i[-1]

                    parent[i[0]] = grid
                    
                    if i[0] not in cost or newcost < cost[i[0]]:
                        cost[i[0]] = newcost
                    else:
                        cost[i[0]] = cost[i[0]]

                    total_cost = cost[i[0]] + heuristic(i[0], end) # total cost = actual cost + future cost

                    queue.put((total_cost, i[0]))
                    


                        
# Main: run algorithm and output 

# Run BFS algorithm
if search_method == 'BFS':

    g = Graph()                             # create graph

    for grid in grids_list:                 # get every grid from grids list and add the next grid as edge
        for a in grid[3:]:
            Next, cost = act(grid[:3], a)   # since BFS does not mind cost, do not add it to graph
            g.addEdge(tuple(grid[:3]), tuple(Next))

    path = BFS(g, tuple(start), tuple(end)) # run BFS

    if path != None:                        # if find the path
        steps = len(path)
        total = steps -1                    # hard code since total cost always less 1 than total steps

        f = open("output.txt", "w")
        f.write(str(total) + "\n")
        f.write(str(steps) + "\n")
        cost = 0
        for i in path[:-1]:                      # ans example: '1 3 1 1\n' first three represent grid, last represent step cost
            ans = ' '.join(map(str,i))
            f.write(ans + ' ' + str(cost) + "\n")
            cost = 1
        f.write(' '.join(map(str, path[-1])) + ' ' + str(cost)) # the last line do not contain '\n'
        f.close()
    else:
        f = open("output.txt", "w")
        f.write("FAIL")
        f.close()

    end_time = time.time()
    print("time= ", end_time-start_time)    # output total time cost


# Run UCS algorithm
if search_method == 'UCS':

    g = Graph()

    for grid in grids_list:                 # same as BFS except add edge with cost
        for a in grid[3:]:
            Next, cost = act(grid[:3],a )
            g.addCost(tuple(grid[:3]), tuple(Next), cost)

    path, total, cpath = UCS(g, tuple(start), tuple(end))

    if path != None:                        # same as BFS except print total steps 
        steps = len(path)

        f = open("output.txt", "w")
        f.write(str(total) + "\n")
        f.write(str(steps) + "\n")
        for i in range(len(path)-1):
            ans = ' '.join(map(str, path[i])) + ' ' + str(cpath[i]) + '\n'
            f.write(ans)
        f.write(' '.join(map(str, path[-1])) + ' ' + str(cpath[-1]))
        f.close()
    else:
        f = open("output.txt", "w")
        f.write("FAIL")
        f.close()

    end_time = time.time()
    print("time= ", end_time-start_time)

# Run A* algorithm  
if search_method == 'A*':                   # same to UCS, except run A* algorithm 

    g = Graph()

    for grid in grids_list: 
        for a in grid[3:]:
            Next, cost = act(grid[:3],a )
            g.addCost(tuple(grid[:3]), tuple(Next), cost)
    
    path, total, cpath = A(g, tuple(start), tuple(end))

    if path != None:
        steps = len(path)
        f = open("output.txt", "w")
        f.write(str(total) + "\n")
        f.write(str(steps) + "\n")
        for i in path[:-1]:
            ans = ' '.join(map(str, i)) + ' ' + str(cpath[i]) + '\n'
            f.write(ans)
        f.write(' '.join(map(str, path[-1])) + ' ' + str(cpath[path[-1]]))
        f.close()
    else:
        f = open("output.txt", "w")
        f.write("FAIL")
        f.close()

    end_time = time.time()
    print("time= ", end_time-start_time)

