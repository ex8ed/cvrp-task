# distance_matrix.py
from app.models import CVRPInstance
import math
from typing import Dict, Tuple


class DistanceMatrix:
    def __init__(self, instance: CVRPInstance):
        self.matrix: Dict[Tuple[int, int], float] = {}
        nodes = list(instance.coords.keys())
        for i in nodes:
            for j in nodes:
                if i == j:
                    self.matrix[(i, j)] = 0.0
                else:
                    x1, y1 = instance.coords[i]
                    x2, y2 = instance.coords[j]
                    self.matrix[(i, j)] = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    
    def get(self, i: int, j: int) -> float:
        return self.matrix[(i, j)]