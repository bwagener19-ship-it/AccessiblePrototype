import time, random, heapq
from data_structures import dijkstra_shortest_path

def make_graph(n, m):
    nodes = [f"n{i}" for i in range(n)]
    edges = {node: [] for node in nodes}
    for _ in range(m):
        u = random.choice(nodes); v = random.choice(nodes)
        if u == v: continue
        w = random.randint(1,50)
        edges[u].append((v,w)); edges[v].append((u,w))
    return edges, nodes[0], nodes[-1]

if __name__ == "__main__":
    edges, s, t = make_graph(2000, 10000)
    t0 = time.perf_counter()
    path, dist = dijkstra_shortest_path(edges, s, t)
    print("time:", time.perf_counter()-t0, "dist:", dist, "pathlen:", len(path) if path else None)
