# CS561 HW1 3D maze
# Zhiqin Lei
# USCID: 1436737564

import math
import collections
import time
from collections import defaultdict
from collections import namedtuple
from collections import deque
from queue import Queue
from queue import PriorityQueue


# read input file
start_time = time.time()
f = open("input6.txt", 'r+')
search_method = f.readline().rstrip('\n') #first line: search method
maze = [int(i) for i in f.readline().rstrip('\n').split(' ')] #second line: size of x,y,z 
start = [int(i) for i in f.readline().rstrip('\n').split(' ')] #third line: entrance grid location
end = [int(i) for i in f.readline().rstrip('\n').split(' ')] #fourth line: exit grid location
num = int(f.readline().rstrip('\n')) #num of grids in maze

grids_list = [] #list of grids and actions eg: [[1, 3, 1, 5], [1, 3, 2, 1, 11]]
grid = [] #list of grids
action = [] #list of actions
for n in range(num):
    grids_list.append([int(i) for i in f.readline().rstrip('\n').split(' ')])
    

#define an act function
def act(g, a):
    #calculate cost
    if 1 <= a & a <= 6:
        c = 10
    elif 7<= a & a <= 18:
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
  
        # default dictionary to store adjacent 
        self.adjacent = defaultdict(list) 
        # use dic to store cost
        self.weights = defaultdict(list)
  
    # function to add an edge to graph 
    def addEdge(self,u,v): 
        self.adjacent[u].append(v) 
    
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
    parent = {}
    visited, queue = set(), [start]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            if node == end:
                path = backtrace(parent, start, end)
                return path
            for n in graph.adjacent[node]: #check near nodes
                if n not in visited:
                    parent[n] = node
                    queue.append(n)
                

# Function of UCS method
def UCS(graph, start, end):
    parent = {}
    visited, queue = set(), PriorityQueue()
    queue.put((0, start, [0]))
    while queue:
        cost, node, cpath= queue.get() 
        if node not in visited:
            visited.add(node)
            if node == end:
                path = backtrace(parent, start, end)
                return path, cost, cpath
            for i in graph.adjacent[node]:
                if i[0] not in visited:
                    parent[i[0]] = node
                    new_path = list(cpath)
                    new_path.append(i[-1])
                    total_cost = cost + i[-1]
                    queue.put((total_cost, i[0], new_path))

def heuristic(a, b):
    (x1, y1, z1) = a
    (x2, y2, z2) = b
    return (math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2))*10

def A(graph, start, end):
    queue = PriorityQueue()
    queue.put(start, 0)
    parent = {}
    cost = {}
    cost[start] = 0

    cpath = {}
    cpath[start] = 0
    while queue:
        node = queue.get()
        if node == end:
            path = backtrace(parent, start, end)
            return (path, cost[end], cpath)
        for i in graph.adjacent[node]:
            newcost = cost[node] + i[-1]
            if i[0] not in cost or newcost < cost[i[0]]:
                cost[i[0]] = newcost
                total_cost = newcost + heuristic(i[0], end)
                parent[i[0]] = node
                cpath[i[0]] = i[-1]
                queue.put(i[0], total_cost)

        

                

# Function of A* method
    #def A(self, start, end):
    
                        
                        

# test command
# BFS commmand

if search_method == 'BFS':
    g = Graph()

    for node in grids_list: #get the next grid of every grid in list
        for a in node[3:]:
            Next, cost = act(node[:3], a)
            g.addEdge(tuple(node[:3]), tuple(Next))

    path = BFS(g, tuple(start), tuple(end))

    if path != None:
        steps = len(path)
        total = steps -1

        f = open("output.txt", "w")
        f.write(str(total) + "\n")
        f.write(str(steps) + "\n")
        cost = 0
        for i in path:
            ans = ' '.join(map(str,i))
            f.write(ans + ' ' + str(cost) + "\n")
            cost = 1
        f.close()
    else:
        f = open("output.txt", "w")
        f.write("FAIL")
        f.close()

    end_time = time.time()
    print("time= ", end_time-start_time)


#UCS test command
if search_method == 'UCS':
    g = Graph()

    for node in grids_list: #get the next grid of every grid in list
        for a in node[3:]:
            Next, cost = act(node[:3],a )
            g.addCost(tuple(node[:3]), tuple(Next), cost)

    path, total, cpath = UCS(g, tuple(start), tuple(end))
    end_time = time.time()
    print("time= ", end_time-start_time)

    if path != None:
        steps = len(path)

        f = open("output.txt", "w")
        f.write(str(total) + "\n")
        f.write(str(steps) + "\n")
        for i in range(len(path)):
            ans = ' '.join(map(str, path[i])) + ' ' + str(cpath[i]) + '\n'
            f.write(ans)
        f.close()
    else:
        f = open("output.txt", "w")
        f.write("FAIL")
        f.close()

    end_time = time.time()
    print("time= ", end_time-start_time)

# A* test command   
if search_method == 'A*':
    g = Graph()

    for node in grids_list: #get the next grid of every grid in list
        for a in node[3:]:
            Next, cost = act(node[:3],a )
            g.addCost(tuple(node[:3]), tuple(Next), cost)
    
    path, total, cpath = A(g, tuple(start), tuple(end))

    if path != None:
        steps = len(path)
        f = open("output.txt", "w")
        f.write(str(total) + "\n")
        f.write(str(steps) + "\n")
        for i in path:
            ans = ' '.join(map(str, i)) + ' ' + str(cpath[i]) + '\n'
            f.write(ans)
        f.close()
    else:
        f = open("output.txt", "w")
        f.write("FAIL")
        f.close()

    end_time = time.time()
    print("time= ", end_time-start_time)

