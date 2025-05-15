def greedy_tsp(distance_matrix, start=0):
    n = len(distance_matrix)
    visited = [False] * n
    path = [start]
    visited[start] = True
    current = start

    for _ in range(n - 1):
        nearest = min(
            ((i, d) for i, d in enumerate(distance_matrix[current]) if not visited[i]),
            key=lambda x: x[1]
        )[0]
        path.append(nearest)
        visited[nearest] = True
        current = nearest

    return path

def two_opt(path, distance_matrix):
    def calculate_total(path):
        return sum(distance_matrix[path[i]][path[i+1]] for i in range(len(path)-1))

    improved = True
    while improved:
        improved = False
        for i in range(1, len(path)-2):
            for j in range(i+1, len(path)):
                if j - i == 1: continue
                new_path = path[:i] + path[i:j][::-1] + path[j:]
                if calculate_total(new_path) < calculate_total(path):
                    path = new_path
                    improved = True
    return path
