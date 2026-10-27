import random
import networkx as nx
class AntColonyRouter:
    def __init__(self, nx_graph, alpha=1.0, beta=2.0, decay=0.1, Q=100.0):
        self.nx_graph = nx_graph
        self.alpha = alpha 
        self.beta = beta   
        self.decay = decay 
        self.Q = Q          
        self.pheromones = {(u, v): 1.0 for u, v in nx_graph.edges()}
    def find_shortest_path(self, source, destination, num_ants=20, iterations=30):
        best_path = None
        best_cost = float('inf')
        for _ in range(iterations):
            all_paths = []
            for _ in range(num_ants):
                path = self._run_single_ant(source, destination)
                if path:
                    cost = sum(self.nx_graph[path[i]][path[i+1]]['weight'] for i in range(len(path)-1))
                    all_paths.append((path, cost))
                    if cost < best_cost:
                        best_cost = cost
                        best_path = path
            for edge in self.pheromones:
                self.pheromones[edge] *= (1.0 - self.decay)
            for path, cost in all_paths:
                for i in range(len(path) - 1):
                    edge = (path[i], path[i+1])
                    if edge in self.pheromones:
                        self.pheromones[edge] += (self.Q / cost)
        return best_path, best_cost
    def _run_single_ant(self, source, destination):
        current_node = source
        path = [current_node]
        visited = {current_node}
        max_steps = len(self.nx_graph.nodes()) * 2 
        steps = 0
        while current_node != destination and steps < max_steps:
            steps += 1
            neighbors = list(self.nx_graph.neighbors(current_node))
            unvisited_neighbors = [n for n in neighbors if n not in visited]
            if not unvisited_neighbors:
                return None  
            probabilities = []
            total = 0.0
            for n in unvisited_neighbors:
                pheromone = self.pheromones.get((current_node, n), 1.0)
                weight = self.nx_graph[current_node][n]['weight']
                heuristic = 1.0 / weight if weight > 0 else 1.0
                value = (pheromone ** self.alpha) * (heuristic ** self.beta)
                probabilities.append(value)
                total += value
            if total == 0:
                next_node = random.choice(unvisited_neighbors)
            else:
                probabilities = [p / total for p in probabilities]
                next_node = random.choices(unvisited_neighbors, weights=probabilities, k=1)[0]
            path.append(next_node)
            visited.add(next_node)
            current_node = next_node
        return path if path[-1] == destination else None


if __name__ == "__main__":
    num_nodes = 10
    p_edge = 0.4
    seed = 42
    raw_graph = nx.gnp_random_graph(num_nodes, p_edge, seed=seed, directed=True)
    while not nx.is_weakly_connected(raw_graph):
        raw_graph = nx.gnp_random_graph(num_nodes, p_edge, directed=True)
    for u, v in raw_graph.edges():
        raw_graph[u][v]['weight'] = random.randint(2, 15)
    source_node = 0
    dest_node = num_nodes - 1
    print(f"--- Routing Matrix Generated [Node {source_node} -> Node {dest_node}] ---")
    aco_router = AntColonyRouter(raw_graph)
    aco_path, aco_cost = aco_router.find_shortest_path(source=source_node, destination=dest_node)
    print(f"ACO Optimized Path : {aco_path} | Total Cost: {aco_cost}")
    try:
        dijkstra_path = nx.dijkstra_path(raw_graph, source_node, dest_node, weight='weight')
        dijkstra_cost = nx.dijkstra_path_length(raw_graph, source_node, dest_node, weight='weight')
        print(f"Dijkstra Ideal Path: {dijkstra_path} | Total Cost: {dijkstra_cost}")
    except nx.NetworkXNoPath:
        print("Dijkstra: No viable path connection found.")
