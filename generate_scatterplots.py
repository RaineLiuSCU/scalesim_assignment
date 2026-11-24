import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('results_a.csv')

predicted = df['predicted_cycles'].values / 100000
total = df['total_cycles'].values / 100000
line = np.array(range(10))
fig, ax = plt.subplots()
ax.scatter(predicted, total, s = 10)
ax.plot(line, linewidth = 1)
ax.set_xlabel("predicted cycles * 10^5")
ax.set_ylabel("total cycles * 10^5")
plt.show()