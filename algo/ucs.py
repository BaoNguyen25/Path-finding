from graph import Cell, Map
import queue
import sys
sys.path.append('../')

INF = int(1e9)

# 4 directions
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]
weight = [1, 1, 1, 1]


def ucs(s, g, w, h, limited):

   # Containers
   direction = [[-1] * w for _ in range(h)]
   distance = [[INF] * w for _ in range(h)]
   pq = queue.PriorityQueue()


   distance[s.y][s.x] = 0
   direction[s.y][s.x] = -2

   # Put start node to priority queue

   pq.put((distance[s.y][s.x], s))

   while not pq.empty():
      u = pq.get()

      # Encounter the goal
      if u[1].x == g.x and u[1].y == g.y:
         break

      # Explore every adjacent nodes
      for i in range(len(dx)):

         # x, y are coordinates of neighbors
         x, y = u[1].x + dx[i], u[1].y + dy[i]

         # Go to the node if it is not limited
         if x in range(w) and y in range(h) and not limited[y][x]:

            # Update cost at neighbor if possible
            if weight[i] + u[0] < distance[y][x]:
               distance[y][x] = weight[i] + u[0]
               direction[y][x] = i
               pq.put((distance[y][x], Cell(x=x, y=y)))
                                
   target_found    = (distance[g.y][g.x] != INF)
   cost        = -1
   path        = None

   if target_found:
      path     = Map.trace_path_by_direction(s=s, g=g, direction=direction)
      cost     = distance[g.y][g.x]

   return target_found, cost, path


