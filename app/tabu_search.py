# tabu_search.py
from collections import deque
import random
from typing import Optional
from app.solution import CVRPSolution, initial_solution
from app.neighborhood import get_neighbors

class TabuSearch:
    def __init__(self, instance, dm, max_iter=1000, tabu_tenure=7, diversification_freq=50):
        self.instance = instance
        self.dm = dm
        self.max_iter = max_iter
        self.tabu_tenure = tabu_tenure
        self.diversification_freq = diversification_freq
        self.best_solution: Optional[CVRPSolution] = None
        self.current_solution: Optional[CVRPSolution] = None
        self.tabu_list = deque(maxlen=tabu_tenure)
    
    def diversify(self, solution: CVRPSolution) -> CVRPSolution:
        """Случайное перемещение 3 клиентов между маршрутами"""
        new_routes = [r.copy() for r in solution.routes]
        for _ in range(3):
            if len(new_routes) < 2:
                break
            r1 = random.randint(0, len(new_routes)-1)
            r2 = random.randint(0, len(new_routes)-1)
            if r1 == r2 or len(new_routes[r1]) == 0:
                continue
            node_idx = random.randint(0, len(new_routes[r1])-1)
            node = new_routes[r1].pop(node_idx)
            new_routes[r2].append(node)
        return CVRPSolution(new_routes, self.instance, self.dm)
    
    def get_move_signature(self, old: CVRPSolution, new: CVRPSolution) -> tuple:
        """Идентификация хода через хэш маршрутов"""
        return tuple(tuple(route) for route in new.routes)
    
    def solve(self) -> CVRPSolution:
        # Инициализация
        self.current_solution = initial_solution(self.instance, self.dm)
        self.best_solution = self.current_solution.copy()
        
        for iter in range(self.max_iter):
            # Диверсификация каждые N итераций
            if iter % self.diversification_freq == 0:
                self.current_solution = self.diversify(self.current_solution)
            
            # Генерация соседей
            neighbors = get_neighbors(self.current_solution)
            if not neighbors:
                continue
                
            # Выбор лучшего допустимого кандидата
            best_candidate = None
            for candidate in sorted(neighbors, key=lambda x: x.cost()):
                move_hash = self.get_move_signature(self.current_solution, candidate)
                if move_hash in self.tabu_list:
                    continue
                best_candidate = candidate
                break
                
            if best_candidate is None:
                continue
                
            # Обновление текущего решения
            self.current_solution = best_candidate
            self.tabu_list.append(self.get_move_signature(self.current_solution, best_candidate))
            
            # Обновление лучшего решения
            if best_candidate.cost() < self.best_solution.cost():
                self.best_solution = best_candidate.copy()
                
        return self.best_solution

def tabu_search(instance, dm, max_iter=1000, tabu_tenure=7):
    ts = TabuSearch(instance, dm, max_iter, tabu_tenure)
    return ts.solve()