# benchmark.py
import csv
import time
import os
from typing import Optional, List
from app.models import CVRPInstance, CVROptimalSolution, BenchmarkResult
from app.tabu_search import tabu_search
from app.distance_matrix import DistanceMatrix


class CVRPSolver:
    def __init__(self, max_iter=1000, tabu_tenure=7, diversification_freq=50):
        self.max_iter = max_iter
        self.tabu_tenure = tabu_tenure
        self.diversification_freq = diversification_freq
        self.results = []
    
    def solve_directory(self, directory: str, output_csv: str = "results.csv"):
        for filename in sorted(os.listdir(directory)):
            if filename.endswith(".vrp"):
                vrp_path = os.path.join(directory, filename)
                sol_path = os.path.join(directory, filename.replace(".vrp", ".sol"))

                instance = CVRPInstance(vrp_path)
                optimal = self._parse_optimal(sol_path)

                start_time = time.time()
                dm = DistanceMatrix(instance)
                solution = tabu_search(
                    instance, 
                    dm,
                    max_iter=self.max_iter,
                    tabu_tenure=self.tabu_tenure
                )
                elapsed = time.time() - start_time

                result = BenchmarkResult()
                result.instance_name = instance.name
                result.problem_type = instance.problem_type
                result.dimension = instance.dimension
                result.found_cost = solution.cost()
                result.execution_time = elapsed
                result.iterations = self.max_iter
                result.num_vehicles = solution.get_num_vehicles()  # Количество автомобилей
                result.vehicle_loads = solution.get_vehicle_loads()  # Загрузка каждого автомобиля

                if optimal and optimal.cost:
                    result.optimal_cost = optimal.cost
                    if optimal.cost > 0:
                        result.deviation_pct = 100 * (result.found_cost - optimal.cost) / optimal.cost

                self.results.append(result)

        self._save_results(output_csv)

    def _parse_optimal(self, sol_path: str) -> Optional[CVROptimalSolution]:
        if os.path.exists(sol_path):
            try:
                return CVROptimalSolution(sol_path)
            except:
                return None
        return None
    
    def _save_results(self, filename: str):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Instance', 'Type', 'Dimension',
                'Optimal Cost', 'Found Cost', 'Deviation (%)',
                'Time (s)', 'Iterations', 'Num Vehicles', 'Vehicle Loads'
            ])

            for result in self.results:
                writer.writerow([
                    result.instance_name,
                    result.problem_type,
                    result.dimension,
                    result.optimal_cost or 'N/A',
                    f"{result.found_cost:.2f}",
                    f"{result.deviation_pct:.2f}" if result.deviation_pct is not None else 'N/A',
                    f"{result.execution_time:.2f}",
                    result.iterations,
                    result.num_vehicles,
                    result.vehicle_loads
                ])