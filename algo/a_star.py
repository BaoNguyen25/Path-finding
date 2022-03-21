from graph import Cell, Map
import queue
import sys
sys.path.append('../')

INF = int(1e9)

# 4 directions
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]
weight = [1, 1, 1, 1]


def a_star(s, g, w, h, limited):

    def heuristic(a, b):
        dx, dy = abs(a.x - b.x), abs(a.y - b.y)
        return dx + dy

    direction = [[-1] * w for _ in range(h)]
    distance = [[INF] * w for _ in range(h)]
    pq = queue.PriorityQueue()

    # Put start to priority queue

    pq.put((heuristic(s, g), s))
    distance[s.y][s.x] = 0
    direction[s.y][s.x] = -2

    while not pq.empty():
        u = pq.get()
        ux, uy = u[1].x, u[1].y

        # Encounter the goal
        if ux == g.x and uy == g.y:
            break

        # Explore every adjacent nodes
        for i in range(len(dx)):

            # x, y are coordinates of neighbors
            x, y = ux + dx[i], uy + dy[i]

            # Go to the node if it is not limited
            if x in range(w) and y in range(h) and not limited[y][x]:

                # Update cost at neighbor if possible
                if weight[i] + u[0] < distance[y][x]:
                     distance[y][x]  = weight[i] + u[0]
                     direction[y][x]  = i
                     priority    = distance[y][x] + heuristic(Cell(x=x, y=y), g)
                     pq.put((priority, Cell(x=x, y=y)))


    target_found = (distance[g.y][g.x] != INF)
    cost = -1
    path = None

    if target_found:
        path = Map.trace_path_by_direction(s=s, g=g, direction=direction)
        cost = distance[g.y][g.x]

    return target_found, cost, path
