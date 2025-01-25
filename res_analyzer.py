import pandas as pd


b = pd.read_csv('benchmark_results_B_2.csv')
print(b['Deviation (%)'].mean())
e = pd.read_csv('benchmark_results_E_2.csv')
print(e['Deviation (%)'].mean())
p = pd.read_csv('benchmark_results_P_2.csv')
print(p['Deviation (%)'].mean())
