"""Implement the six graph methods and your route helper. See the README at the repository root."""
import sys
sys.setrecursionlimit(200000)

def dsu(request):
    n = request["n"]
    operations = request["operations"]

    parent = list(range(n))
    size = [1] * n
    components = n
    largest = 1 if n > 0 else 0

    def find(i):
        path = []
        while parent[i] != i:
            path.append(i)
            i = parent[i]
        for node in path:
            parent[node] = i
        return i

    def union(i, j):
        nonlocal components, largest
        root_i = find(i)
        root_j = find(j)
        
        if root_i != root_j:
            if size[root_i] < size[root_j]:
                root_i, root_j = root_j, root_i
            parent[root_j] = root_i
            size[root_i] += size[root_j]
            components -= 1
            if size[root_i] > largest:
                largest = size[root_i]

    states = []
    for u, v in operations:
        if n > 0:
            union(u, v)
        states.append([components, largest])

    return {"states": states}
def kruskal(request):
    n = request["n"]
    edges = request["edges"]

    if n <= 0:
        return {"cost": 0, "edge_ids": [], "components": 0}


    indexed_edges = [(w, orig_id, u, v) for orig_id, (u, v, w) in enumerate(edges)]
    indexed_edges.sort(key=lambda x: (x[0], x[1]))

    parent = list(range(n))
    size = [1] * n

    def find(i):
        path = []
        while parent[i] != i:
            path.append(i)
            i = parent[i]
        for node in path:
            parent[node] = i
        return i

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            if size[root_i] < size[root_j]:
                root_i, root_j = root_j, root_i
            parent[root_j] = root_i
            size[root_i] += size[root_j]
            return True
        return False

    cost = 0
    edge_ids = []
    components = n

    for w, orig_id, u, v in indexed_edges:
        if union(u, v):
            cost += w
            edge_ids.append(orig_id)
            components -= 1

    return {"cost": cost, "edge_ids": edge_ids, "components": components}


import heapq

def prim(request):
    n = request["n"]
    edges = request["edges"]

    if n <= 0:
        return {"cost": 0, "edge_ids": [], "components": 0}

    adj = [[] for _ in range(n)]
    for orig_id, (u, v, w) in enumerate(edges):
        adj[u].append((v, w, orig_id))
        adj[v].append((u, w, orig_id))

    visited = [False] * n
    total_cost = 0
    edge_ids = []
    components = 0

    for start in range(n):
        if not visited[start]:
            components += 1
            visited[start] = True
            min_heap = []
            for v, w, orig_id in adj[start]:
                heapq.heappush(min_heap, (w, orig_id, start, v))
            
            while min_heap:
                w, orig_id, u, v = heapq.heappop(min_heap)
                if visited[v]:
                    continue
                visited[v] = True
                total_cost += w
                edge_ids.append(orig_id)
                
                for next_v, next_w, next_orig_id in adj[v]:
                    if not visited[next_v]:
                        heapq.heappush(min_heap, (next_w, next_orig_id, v, next_v))

    return {"cost": total_cost, "edge_ids": edge_ids, "components": components}


def scc(request):
    n = request["n"]
    edges = request["edges"]

    if n <= 0:
        return {"component": [], "condensation": []}

    adj = [[] for _ in range(n)]
    rev_adj = [[] for _ in range(n)]
    
    for u, v in edges:
        if 0 <= u < n and 0 <= v < n:
            adj[u].append(v)
            rev_adj[v].append(u)

    visited = [False] * n
    order = []

    def dfs1(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)

    for i in range(n):
        if not visited[i]:
            dfs1(i)

    visited = [False] * n
    component = [-1] * n
    comp_id = 0
    scc_roots = []

    def dfs2(u, cid):
        visited[u] = True
        component[u] = cid
        for v in rev_adj[u]:
            if not visited[v]:
                dfs2(v, cid)

    for u in reversed(order):
        if not visited[u]:
            scc_roots.append(u)
            dfs2(u, comp_id)
            comp_id += 1

    cond_set = set()
    for u, v in edges:
        if 0 <= u < n and 0 <= v < n:
            cu = component[u]
            cv = component[v]
            if cu != cv:
                cond_set.add((cu, cv))

    condensation = sorted(list(cond_set))

    return {"component": component, "condensation": condensation}



def topo(request):
    n = request["n"]
    edges = request["edges"]

    if n <= 0:
        return {"acyclic": True, "order": []}

    adj = [[] for _ in range(n)]
    for u, v in edges:
        if 0 <= u < n and 0 <= v < n:
            adj[u].append(v)

    state = [0] * n
    order = []
    is_acyclic = True

    def dfs(u):
        nonlocal is_acyclic
        state[u] = 1
        for v in adj[u]:
            if state[v] == 1:
                is_acyclic = False
                return
            elif state[v] == 0:
                dfs(v)
                if not is_acyclic:
                    return
        state[u] = 2
        order.append(u)

    for i in range(n):
        if state[i] == 0:
            dfs(i)
            if not is_acyclic:
                return {"acyclic": False, "order": []}

    order.reverse()
    return {"acyclic": True, "order": order}



def dag(request):
    n = request["n"]
    source = request["source"]
    edges = request["edges"]

    if n <= 0:
        return {"acyclic": True, "distance": [], "parent_edge": []}

    adj = [[] for _ in range(n)]
    for orig_id, (u, v, w) in enumerate(edges):
        if 0 <= u < n and 0 <= v < n:
            adj[u].append((v, w, orig_id))

    state = [0] * n
    order = []
    is_acyclic = True

    def dfs(u):
        nonlocal is_acyclic
        state[u] = 1
        for v, w, orig_id in adj[u]:
            if state[v] == 1:
                is_acyclic = False
                return
            elif state[v] == 0:
                dfs(v)
                if not is_acyclic:
                    return
        state[u] = 2
        order.append(u)

    for i in range(n):
        if state[i] == 0:
            dfs(i)
            if not is_acyclic:
                return {"acyclic": False, "distance": [], "parent_edge": []}

    order.reverse()

    distance = [None] * n
    parent_edge = [-1] * n

    if 0 <= source < n:
        distance[source] = 0

        for u in order:
            if distance[u] is not None:
                for v, w, orig_id in adj[u]:
                    new_dist = distance[u] + w
                    if distance[v] is None or new_dist < distance[v]:
                        distance[v] = new_dist
                        parent_edge[v] = orig_id

    return {"acyclic": True, "distance": distance, "parent_edge": parent_edge}


def reconstruct_route(source, target, parent_edge, edges):
    """Route-reconstruction helper."""
    if source == target:
        return [source]
    
    path = [target]
    curr = target
    while curr != source:
        p_edge = parent_edge[curr]
        if p_edge == -1:
            return [] 
        u, v, w = edges[p_edge]
        path.append(u)
        curr = u
    path.reverse()
    return path
