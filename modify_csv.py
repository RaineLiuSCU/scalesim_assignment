import pandas as pd

df = pd.read_csv('results.csv')

arrayHeights = [32,64,128,256]
arrayWidths = [32,64,128,256]
stationary = ["ws", "is", "os"]

flows = []
heights = []
widths = []
pes = []
names = []
workload = ["gemm" for x in range(48)]
for flow in stationary:
    for height in arrayHeights:
        for width in arrayWidths:
            names.append("gemm_"+str(height)+"x"+str(width)+"_"+flow)
            flows.append(flow)
            heights.append(height)
            widths.append(width)
            pes.append(height*width)

df['dataflow'] = flows
df['height'] = heights
df['width'] = widths
df['pes'] = pes
df['run_name'] = names
df['workload'] = workload
df = df.drop(columns=['Unnamed: 5'])
df['total_cycles'] = df['Total Cycles']+1
df['predicted_cycles'] = df[' Predicted Cycles']
df['stall_cycles'] = df[' Stall Cycles']
df['util'] = df[' Overall Util %']
df['mapping_eff'] = df[' Mapping Efficiency %']

df = df[['workload', 'run_name', 'dataflow', 'height', 'width', 'pes', 'predicted_cycles', 'total_cycles', 'stall_cycles', 'util', 'mapping_eff']]

print(df.iloc[[0,1,2,3,4,5,6]])
df.to_csv('results_a.csv')