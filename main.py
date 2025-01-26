from app.benchmark import CVRPSolver

if __name__ == "__main__":
    solver = CVRPSolver(max_iter=1500, tabu_tenure=10, diversification_freq=500)
    solver.solve_directory(
        directory="./data/B",
        output_csv="./benchmark_results_B_3.csv"
    )
