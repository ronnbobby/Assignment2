from collections import deque


def bfs(capacity, source, sink, parent):
    n = len(capacity)
    visited = [False] * n

    queue = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()

        for v in range(n):
            if not visited[v] and capacity[u][v] > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u

                if v == sink:
                    return True

    return False


def max_flow(capacity, source, sink):
    parent = [-1] * len(capacity)
    flow = 0

    while bfs(capacity, source, sink, parent):

        # Find minimum capacity in the path
        path_flow = float('inf')
        v = sink

        while v != source:
            u = parent[v]
            path_flow = min(path_flow, capacity[u][v])
            v = u

        # Update residual graph
        v = sink
        while v != source:
            u = parent[v]
            capacity[u][v] -= path_flow
            capacity[v][u] += path_flow
            v = u

        flow += path_flow

    return flow


def crabGraphs(n, T, graph):

    # Total nodes:
    # n nodes for heads
    # n nodes for feet
    # 1 source + 1 sink
    size = 2 * n + 2

    source = 2 * n
    sink = 2 * n + 1

    capacity = [[0] * size for _ in range(size)]

    degree = [0] * n

    # Create edges between head-copy and feet-copy
    for u, v in graph:
        u -= 1
        v -= 1

        # u can be head, v can be foot
        capacity[u][n + v] = 1

        # v can be head, u can be foot
        capacity[v][n + u] = 1

        degree[u] += 1
        degree[v] += 1

    # Source -> Head nodes
    for i in range(n):
        capacity[source][i] = min(T, degree[i])

    # Feet nodes -> Sink
    for i in range(n):
        capacity[n + i][sink] = 1

    return max_flow(capacity, source, sink)


# Input
C = int(input())

for _ in range(C):
    N, T, M = map(int, input().split())

    graph = []

    for _ in range(M):
        u, v = map(int, input().split())
        graph.append([u, v])

    result = crabGraphs(N, T, graph)

    print(result)