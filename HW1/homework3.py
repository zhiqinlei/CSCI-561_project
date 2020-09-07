# CS561 HW1 3D maze
# Zhiqin Lei
# USCID: 1436737564

import math
import collections
from collections import defaultdict
from collections import namedtuple
from collections import deque
from queue import Queue
from queue import PriorityQueue



# read input file
f = open("input.txt", 'r+')
search_method = f.readline().rstrip('\n') #first line: search method
maze = [int(i) for i in f.readline().rstrip('\n').split(' ')] #second line: size of x,y,z 
start = [int(i) for i in f.readline().rstrip('\n').split(' ')] #third line: entrance grid location
end = [int(i) for i in f.readline().rstrip('\n').split(' ')] #fourth line: exit grid location
num = int(f.readline().rstrip('\n')) #num of grids in maze

grids_list = [] #list of grids eg: [[1, 3, 1, 5], [1, 3, 2, 1, 11]]
Point = namedtuple('Point', ['x','y','z'])
s = Point(start[0],start[1],start[2])

grid = []
action = []
for n in range(num):
    grids_list.append([int(i) for i in f.readline().rstrip('\n').split(' ')])
    grid.append(grids_list[n][:3])
    action.append(grids_list[n][3:])

#define an act function
def act(g, a):
    #calculate cost
    if 1 <= a & a <= 6:
        c = 1
    elif 7<= a & a <= 18:
        c = math.sqrt(2)
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
    
    def addCost (self,u,c):
        self.weights[u].append(c)
    
    def getCost (self, u):
        return self.weights[u][0]

# Function of BFS method
    def BFS(self, start, end): 
        visited, queue = set(), [[start]]
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node == end:
                print(path)
                return path
            if node not in visited:
                for n in self.graph[node]: #check near nodes
                    new_path = list(path)
                    new_path.append(n)
                    queue.append(new_path)
                visited.add(node)

# Function of UCS method
    def UCS(self, start, end):
        visited, queue = set(), PriorityQueue()
        queue.put((0, [start]))
        while queue:
            cost, path = queue.get()
            node = path[-1]
            if node == end:
                return path
            if node not in visited:
                for i in self.graph[node]:
                    total_cost = cost + self.getCost(node)
                    queue.put((total_cost, path+[i]))
                visited.add(node)
            
            
           # if node not in visited:
                #print(node)
                #visited.add(node)
                #if node == end:
                    #print('end')
                    #return 
                #for i in self.graph[node]:
                    #if i not in visited:
                        #total_cost = cost + self.getCost(node)
                        #queue.put((total_cost, i))
                        
                        

# test command
# BFS commmand
#g = Graph()

#for i in range(len(grids_list)): #get the next grid of every grid in list
    #for j in action[i]:
        #Next = act(grid[i][:],j)
        #if Next in grid: # check if next grid is reachable
            #g.addEdge(i, grid.index(Next))

#path = g.BFS(grid.index(start), grid.index(end))
#steps = len(path)
#total = steps -1
#print(total)
#print (steps)
#for i in path:
    #print (grid[i])

g = Graph()

for i in range(len(grids_list)): #get the next grid of every grid in list
    for j in action[i]:
        Next, cost = act(grid[i][:],j)
        if Next in grid: # check if next grid is reachable
            g.addEdge(i, grid.index(Next))
            g.addCost(i, cost)

g.UCS(grid.index(start), grid.index(end))


path = g.UCS(grid.index(start), grid.index(end))
#steps = len(path)
#total = steps -1
#print(total)
#print (steps)
for i in path:
    print (grid[i])

    

