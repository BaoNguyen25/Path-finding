from graph import Cell, Map
from collections import deque
import sys
sys.path.append('../')


# 4 directions
dx       = [0, 0, 1, -1]
dy       = [1, -1, 0, 0]
weight   = [1, 1, 1, 1]

def bfs(s, g, w, h, limited):

   # Containers
   visited = [[False] * w for _ in range(h)]
   distance = [[-1] * w for _ in range(h)]
   direction  = [[-1] * w for _ in range(h)]
   q = deque()
   
   # Append start node to queue
   q.append(s)

   visited[s.y][s.x] = True
   distance[s.y][s.x]    = 0
   direction[s.y][s.x]    = -2
 
   while q:
      u = q.popleft()
     
      # Encounter the goal
      if u.x == g.x and u.y == g.y:
         break
      
      # Explore every adjacent nodes
      for i in range(len(dx)):
         x, y        = u.x + dx[i], u.y + dy[i]

         # Check if the adjacent node is valid
         if x in range(w) and y in range(h) and not visited[y][x]:
            visited[y][x]     = True

            # Go to the node if it is not limited
            if not limited[y][x]:
               distance[y][x]     = weight[i] + distance[u.y][u.x]
               direction[y][x]     = i
               q.append(Cell(x=x, y=y))

   path = None
   cost = -1

   if visited[g.y][g.x]:
      path     = Map.trace_path_by_direction(s=s, g=g, direction=direction)
      cost     = distance[g.y][g.x]
   
   return visited[g.y][g.x], cost, path
