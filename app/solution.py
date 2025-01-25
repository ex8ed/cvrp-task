# solution.py
from typing import List, Optional
from app.models import CVRPInstance
from app.distance_matrix import DistanceMatrix

class CVRPSolution:
    def __init__(self, routes: List[List[int]], instance: CVRPInstance, dm: DistanceMatrix):
        self.routes = routes
        self.instance = instance
        self.dm = dm
        self._cost: Optional[float] = None
        
    def cost(self) -> float:
        if self._cost is None:
            total = 0.0
            for route in self.routes:
                if not route:
                    continue
                current = self.instance.depot
                for node in route:
                    total += self.dm.get(current, node)
                    current = node
                total += self.dm.get(current, self.instance.depot)
            self._cost = total
        return self._cost
    
    def copy(self):
        return CVRPSolution([r.copy() for r in self.routes], self.instance, self.dm)

def initial_solution(instance: CVRPInstance, dm: DistanceMatrix) -> CVRPSolution:
    unvisited = list(instance.demands.keys())
    unvisited.remove(instance.depot)
    
    routes = []
    current_route = []
    current_load = 0
    
    while unvisited:
        candidates = []
        for node in unvisited:
            demand = instance.demands[node]
            if current_load + demand <= instance.capacity:
                candidates.append(node)
        
        if not candidates:
            routes.append(current_route)
            current_route = []
            current_load = 0
            continue
        
        last = instance.depot if not current_route else current_route[-1]
        next_node = min(candidates, key=lambda x: dm.get(last, x))
        
        current_route.append(next_node)
        current_load += instance.demands[next_node]
        unvisited.remove(next_node)
    
    if current_route:
        routes.append(current_route)
    
    return CVRPSolution(routes, instance, dm)