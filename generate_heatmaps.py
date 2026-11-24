import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def create_heatmap(heights, widths, values, ax, title):
    im = ax.imshow(values)
    ax.set_xticks(range(len(widths)), labels = widths, rotation = 45, rotation_mode="xtick")
    ax.set_yticks(range(len(heights)), labels = heights)
    ax.set_xlabel("width")
    ax.set_ylabel("height")
    for i in range(len(heights)):
        for j in range(len(widths)):
            text = ax.text(j, i, values[i,j],ha="center", va="center", color="w")
    ax.set_title(title)


df = pd.read_csv('results_a.csv')
df = df[['total_cycles','util', 'width', 'height']]

df_ws = df.iloc[:16]
ws_cycles = df_ws['total_cycles'].values.reshape((4,4))
ws_util = df_ws['util'].values.reshape((4,4))
ws_util = np.round(ws_util, 2)

df_is = df.iloc[16:32]
is_cycles = df_is['total_cycles'].values.reshape((4,4))
is_util = df_is['util'].values.reshape((4,4))
is_util = np.round(is_util, 2)

df_os = df.iloc[32:48]
os_cycles = df_os['total_cycles'].values.reshape((4,4))
os_util = df_os['util'].values.reshape((4,4))
os_util = np.round(os_util, 2)

arrayHeights = [32,64,128,256]
arrayWidths = [32,64,128,256]

fig, ax = plt.subplots(2,3)
create_heatmap(arrayHeights, arrayWidths, ws_cycles, ax[0,0], "WS total cycles")
create_heatmap(arrayHeights, arrayWidths, ws_util, ax[1,0], "WS util %")
create_heatmap(arrayHeights, arrayWidths, is_cycles, ax[0,1], "IS total cycles")
create_heatmap(arrayHeights, arrayWidths, is_util, ax[1,1], "IS util %")
create_heatmap(arrayHeights, arrayWidths, os_cycles, ax[0,2], "OS total cycles")
create_heatmap(arrayHeights, arrayWidths, os_util, ax[1,2], "OS util %")
plt.show()