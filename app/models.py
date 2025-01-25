# models.py
from typing import Dict, List, Optional, Tuple

class CVRPInstance:
    def __init__(self, file_path: str):
        self.name = ""
        self.problem_type = ""
        self.dimension = 0
        self.capacity = 0
        self.depot = 0
        self.coords: Dict[int, Tuple[float, float]] = {}
        self.demands: Dict[int, int] = {}
        
        with open(file_path, 'r') as f:
            section = None
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith("NAME"):
                    self.name = line.split(":")[1].strip()
                    self.problem_type = self.name.split('-')[0]
                elif line.startswith("DIMENSION"):
                    self.dimension = int(line.split(":")[1].strip())
                elif line.startswith("CAPACITY"):
                    self.capacity = int(line.split(":")[1].strip())
                elif line.startswith("NODE_COORD_SECTION"):
                    section = "COORDS"
                elif line.startswith("DEMAND_SECTION"):
                    section = "DEMANDS"
                elif line.startswith("DEPOT_SECTION"):
                    section = "DEPOT"
                elif line == "EOF":
                    break
                else:
                    if section == "COORDS":
                        parts = line.split()
                        node = int(parts[0])
                        x, y = map(float, parts[1:])
                        self.coords[node] = (x, y)
                    elif section == "DEMANDS":
                        parts = line.split()
                        node = int(parts[0])
                        demand = int(parts[1])
                        self.demands[node] = demand
                    elif section == "DEPOT":
                        if line != "-1":
                            self.depot = int(line.strip())

class CVROptimalSolution:
    def __init__(self, file_path: str):
        self.cost: Optional[float] = None
        self.routes: List[List[int]] = []
        
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith("Cost"):
                    self.cost = float(line.split()[-1])
                elif line.startswith("Route"):
                    nodes = list(map(int, line.split(":")[1].strip().split()))
                    self.routes.append(nodes)

class BenchmarkResult:
    def __init__(self):
        self.instance_name = ""
        self.problem_type = ""
        self.dimension = 0
        self.optimal_cost: Optional[float] = None
        self.found_cost: Optional[float] = None
        self.deviation_pct: Optional[float] = None
        self.execution_time: Optional[float] = None
        self.iterations = 0