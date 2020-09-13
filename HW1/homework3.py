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
f = open("input.txt", 'r+')
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
  
        # default dictionary to store graph 
        self.graph = defaultdict(list) 
        # use dic to store cost
        self.weights = defaultdict(list)
  
    # function to add an edge to graph 
    def addEdge(self,u,v): 
        self.graph[u].append(v) 
    
    def addCost(self,u,v,c):
        self.graph[u].append([v,c])
    
    def getCost (self, u):
        return self.graph[u][0][-1]

# Function of BFS method
    def BFS(self, start, end): 
        visited, queue = set(), [[start]]
        while queue:
            path = queue.pop(0)
            node = path[-1]
            
            if node not in visited:
                visited.add(node)
                if node == end:
                    return path
                for n in self.graph[node]: #check near nodes
                    if n not in visited:
                        new_path = list(path)
                        new_path.append(n)
                        queue.append(new_path)
                

# Function of UCS method
    def UCS(self, start, end):
        visited, queue = set(), PriorityQueue()
        queue.put((0, [[start, 0]]))
        total_cost = 0
        while queue:
            cost, path = queue.get()
            node = path[-1][0]
            if node not in visited:
                visited.add(node)
                if node == end:
                    return path, cost
                for i in self.graph[node]:
                    if i[0] not in visited:
                        total_cost = cost + i[-1]
                        queue.put((total_cost, path+[i]))

                

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

    path = g.BFS(tuple(start), tuple(end))
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

    end_time = time.time()
    print("time= ", end_time-start_time)


#UCS test command
if search_method == 'UCS':
    g = Graph()

    for node in grids_list: #get the next grid of every grid in list
        for a in node[3:]:
            Next, cost = act(node[:3],a )
            g.addCost(tuple(node[:3]), tuple(Next), cost)

    path, total = g.UCS(tuple(start), tuple(end))
    steps = len(path)

    f = open("output.txt", "w")
    f.write(str(total) + "\n")
    f.write(str(steps) + "\n")
    for i in path:
        ans = ' '.join(map(str, i[0])) + ' ' + str(i[-1]) + '\n'
        f.write(ans)
    f.close()
    
    end_time = time.time()
    print("time= ", end_time-start_time)

    


