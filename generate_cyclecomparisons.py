import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('results_project_total.csv')

df = df[['Matrix Size', 'Panel Size', 'Is Baseline?', 'Cycles Per GEMM']]
df = df.sort_values(by = [ "Matrix Size","Panel Size"])

baseline_4096 = df[df['Is Baseline?'].eq(True) & df['Matrix Size'].eq(4096)]
baseline_8192 = df[df['Is Baseline?'].eq(True) & df['Matrix Size'].eq(8192)]
ring_4096 = df[df['Is Baseline?'].eq(False) & df['Matrix Size'].eq(4096)]
ring_8192 = df[df['Is Baseline?'].eq(False) & df['Matrix Size'].eq(8192)]


plt.plot(baseline_4096['Panel Size'].values, baseline_4096['Cycles Per GEMM'].values, label = 'baseline, 4096x4096')
plt.plot(baseline_8192['Panel Size'].values, baseline_8192['Cycles Per GEMM'].values, label = 'baseline, 8192x8192')
plt.plot(ring_4096['Panel Size'].values, ring_4096['Cycles Per GEMM'].values, label = 'ring, 4096x4096')
plt.plot(ring_8192['Panel Size'].values, ring_8192['Cycles Per GEMM'].values, label = 'ring, 8192x8192')

plt.xlabel("Panel Size")
plt.ylabel("Total # Cycles")
plt.legend()
plt.show()

