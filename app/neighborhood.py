# neighborhood.py
from typing import List
from app.solution import CVRPSolution


def is_valid(solution: CVRPSolution) -> bool:
    for route in solution.routes:
        if sum(solution.instance.demands[node] for node in route) > solution.instance.capacity:
            return False
    return True


def repair(solution: CVRPSolution) -> CVRPSolution:
    repaired_routes = []
    for route in solution.routes:
        current_load = 0
        new_route = []
        for node in route:
            node_demand = solution.instance.demands[node]
            if current_load + node_demand > solution.instance.capacity:
                if new_route:  # Сохраняем текущий маршрут
                    repaired_routes.append(new_route)
                new_route = [node]
                current_load = node_demand
            else:
                new_route.append(node)
                current_load += node_demand
        if new_route:
            repaired_routes.append(new_route)
    return CVRPSolution(repaired_routes, solution.instance, solution.dm)


def relocate_move(solution: CVRPSolution) -> List[CVRPSolution]:
    neighbors = []
    for i in range(len(solution.routes)):
        for j in range(len(solution.routes)):
            if i == j or not solution.routes[i]:
                continue
            for idx in range(len(solution.routes[i])):
                new_routes = [r.copy() for r in solution.routes]
                node = new_routes[i].pop(idx)
                new_routes[j].append(node)
                neighbor = CVRPSolution(new_routes, solution.instance, solution.dm)
                neighbors.append(neighbor)
    return neighbors


def swap_move(solution: CVRPSolution) -> List[CVRPSolution]:
    neighbors = []
    for i in range(len(solution.routes)):
        for j in range(i+1, len(solution.routes)):
            if len(solution.routes[i]) == 0 or len(solution.routes[j]) == 0:
                continue
            for idx_i in range(len(solution.routes[i])):
                for idx_j in range(len(solution.routes[j])):
                    new_routes = [r.copy() for r in solution.routes]
                    new_routes[i][idx_i], new_routes[j][idx_j] = new_routes[j][idx_j], new_routes[i][idx_i]
                    neighbors.append(CVRPSolution(new_routes, solution.instance, solution.dm))
    return neighbors


def two_opt_move(solution: CVRPSolution) -> List[CVRPSolution]:
    neighbors = []
    for r_idx, route in enumerate(solution.routes):
        if len(route) < 2:
            continue
        for i in range(len(route)):
            for j in range(i+1, len(route)):
                new_route = route[:i] + route[i:j+1][::-1] + route[j+1:]
                new_routes = [r.copy() for r in solution.routes]
                new_routes[r_idx] = new_route
                neighbors.append(CVRPSolution(new_routes, solution.instance, solution.dm))
    return neighbors


def cross_exchange_move(solution: CVRPSolution, seg_length=2) -> List[CVRPSolution]:
    neighbors = []
    for r1_idx, r1 in enumerate(solution.routes):
        for r2_idx, r2 in enumerate(solution.routes):
            if r1_idx == r2_idx or len(r1) < seg_length or len(r2) < seg_length:
                continue
            for i in range(len(r1) - seg_length + 1):
                for j in range(len(r2) - seg_length + 1):
                    new_r1 = r1[:i] + r2[j:j+seg_length] + r1[i+seg_length:]
                    new_r2 = r2[:j] + r1[i:i+seg_length] + r2[j+seg_length:]
                    new_routes = [r.copy() for r in solution.routes]
                    new_routes[r1_idx] = new_r1
                    new_routes[r2_idx] = new_r2
                    neighbors.append(CVRPSolution(new_routes, solution.instance, solution.dm))
    return neighbors


def get_neighbors(solution: CVRPSolution) -> List[CVRPSolution]:
    neighbors = []
    
    neighbors += relocate_move(solution)
    neighbors += swap_move(solution)
    neighbors += two_opt_move(solution)
    neighbors += cross_exchange_move(solution)
    
    valid_neighbors = []
    for neighbor in neighbors:
        if is_valid(neighbor):
            valid_neighbors.append(neighbor)
        else:
            repaired = repair(neighbor)
            if is_valid(repaired):
                valid_neighbors.append(repaired)
    
    return valid_neighbors