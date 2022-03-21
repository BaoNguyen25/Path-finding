from graph import Cell, Map
import queue
import sys
sys.path.append('../')

# 4 directions
dx       = [0, 0, 1, -1]
dy       = [1, -1, 0, 0]
weight   = [1, 1, 1, 1]


def greedy_bfs(s, g, w, h, limited):

    def heuristic(a, b):
        dx, dy = abs(a.x - b.x), abs(a.y - b.y)
        return dx + dy

    # Containers
    visited = [[False] * w for _ in range(h)]
    distance = [[-1] * w for _ in range(h)]
    direction = [[-1] * w for _ in range(h)]
    pq = queue.PriorityQueue()

    visited[s.y][s.x]   = True
    direction[s.y][s.x]      = -2
    distance[s.y][s.x]      = 0

    # Put start node to priority queue

    pq.put((heuristic(s, g), s))

    while not pq.empty():
        u         = pq.get()
        ux, uy    = u[1].x, u[1].y

        # Encounter the goal
        if ux == g.x and uy == g.y:
            break

        # Explore every adjacent nodes
        for i in range(len(dx)):

            # x, y are coordinates of neighbors
            x, y  = ux + dx[i], uy + dy[i]

            if x in range(w) and y in range(h) and not visited[y][x]:
                visited[y][x] = True
                
                # Go to the node if it is not limit
                if not limited[y][x]:
                    direction[y][x]   = i
                    distance[y][x]   = weight[i] + distance[uy][ux]
                    priority     = heuristic(Cell(x=x, y=y), g)
                    pq.put((priority, Cell(x=x, y=y)))
           
    cost    = -1
    path    = None
         
    if visited[g.y][g.x]:
       path    = Map.trace_path_by_direction(s=s, g=g, direction=direction)
       cost    = distance[g.y][g.x]
       
    return visited[g.y][g.x], cost, path
