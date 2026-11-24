import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv 

f = open('B2history.csv', 'r')
reader = csv.reader(f)
history = next(reader)

history = np.array(history, dtype = int)
plt.plot(range(27), history)
plt.show()