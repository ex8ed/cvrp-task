import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


b = pd.read_csv('./csv/benchmark_results_B_2.csv')
e = pd.read_csv('./csv/benchmark_results_E_2.csv')
p = pd.read_csv('./csv/benchmark_results_P_2.csv')

sns.set_theme(style="whitegrid", palette="deep", font_scale=1.2)
colors = {'B': '#1f77b4', 'E': '#ff7f0e', 'P': '#2ca02c'}


def plot_combined(task_type, data, color):
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    sns.lineplot(data=data, x='Dimension', y='Time (s)', 
                 marker='o', color=color, ax=ax1, label='Время')
    ax1.set_xlabel('Размерность задачи')
    ax1.set_ylabel('Время (сек)', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    sns.lineplot(data=data, x='Dimension', y='Deviation (%)', 
                 marker='s', color='purple', ax=ax2, label='Отклонение')
    ax2.set_ylabel('Отклонение (%)', color='purple')
    ax2.tick_params(axis='y', labelcolor='purple')
    
    plt.title(f'Производительность для типа {task_type}')
    fig.legend(loc='upper left', bbox_to_anchor=(0.12, 0.88))
    plt.tight_layout()
    plt.savefig(f'combined_{task_type}.png', dpi=300)
    plt.close()

plot_combined('B', b, colors['B'])
plot_combined('E', e, colors['E'])
plot_combined('P', p, colors['P'])

plt.figure(figsize=(10, 6))

avg_times = {
    'B': b['Time (s)'].mean(),
    'E': e['Time (s)'].mean(),
    'P': p['Time (s)'].mean()
}

df_avg = pd.DataFrame({
    'Task Type': list(avg_times.keys()),
    'Average Time': list(avg_times.values())
})

bar = sns.barplot(data=df_avg, x='Task Type', y='Average Time', 
                 palette=colors.values(), alpha=0.8)

for p in bar.patches:
    bar.annotate(f"{p.get_height():.1f} сек", 
                 (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='center', 
                 xytext=(0, 9), 
                 textcoords='offset points')

plt.title('Среднее время выполнения по типам задач')
plt.xlabel('Тип задачи')
plt.ylabel('Среднее время (сек)')
plt.ylim(0, max(avg_times.values()) * 1.1)
plt.tight_layout()
plt.savefig('task_type_comparison.png', dpi=300)
plt.close()

