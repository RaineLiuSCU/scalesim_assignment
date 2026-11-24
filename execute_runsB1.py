from pathlib import Path
import pandas as pd
from math import ceil
from scalesim import scale
import csv 

arrayHeight = [128, 104, 88]
arrayWidth = [120, 144, 72]
stationary = "os"
IfmapSramSzkB = [32, 128, 1024]
FilterSramSzkB = [32, 128, 1024]
OfmapSramSzkB = [32, 128, 1024]
mode =["USER", "CALC"]
work = [512, 1280, 1152] # M,N,K static

filename = "results_b.csv"
results = open(filename,'a+')
writer = csv.writer(results)

filename2 = "results_b1.csv"
results2 = open(filename2,'a+')
writer2 = csv.writer(results2)

def predict_total_cycles(height, width, flow):
    if flow == "os":
        return ceil(work[0]/height) * ceil(work[1]/width) * (work[2] + height + width - 2)
    elif flow == "ws":
        return ceil(work[2]/height) * ceil(work[1]/width) * (work[0] + height + width - 2)
    elif flow == "is":
        return ceil(work[0]/height) * ceil(work[2]/width) * (work[1] + height + width - 2)
    else:
        print("Unknown flow; returning -1")
        return -1

run_dir = Path('runs_labB')
run_top = Path('topologies_lab') / "partA.csv"
run_layout = Path('layouts/conv_nets') / "test.csv"
run_results = Path('run_resultsB')

for item in mode:
    for i in range(3):
        name = "gemmB_"+str(arrayHeight[i])+"_"+str(arrayWidth[i])+"_"+str(IfmapSramSzkB[i])+"_"+str(FilterSramSzkB[i])+"_"+str(OfmapSramSzkB[i])+"_"+item        
        config_path = run_dir / (name + ".cfg")
        run = scale.scalesim(save_disk_space=True, config=config_path.absolute().as_posix(), topology=run_top.absolute().as_posix(), layout=run_layout.absolute().as_posix(), input_type_gemm=True)
        run.run_scale(top_path='run_resultsB')

        data = ["gemm", name, "os", arrayHeight[i], arrayWidth[i], arrayHeight[i]*arrayWidth[i], predict_total_cycles(arrayHeight[i], arrayWidth[i], "os")]    

        df = pd.read_csv(run_results / name / "COMPUTE_REPORT.csv")
        results_extracted = df[[' Total Cycles', ' Stall Cycles', ' Overall Util %', ' Mapping Efficiency %']].values.tolist()    
        total_cycles = df[[' Total Cycles (incl. prefetch)']].values.tolist()  
        total_cycles = total_cycles[0]
        results_extracted = results_extracted[0]  

        data2 = [IfmapSramSzkB[i], FilterSramSzkB[i], OfmapSramSzkB[i]]

        data.extend(results_extracted)
        data.extend(data2)
        data.extend(total_cycles)
        data.append(item)
        writer.writerow(data)

        df2 = pd.read_csv(run_results / name / "BANDWIDTH_REPORT.csv")
        results_extracted2 = df2[[' Avg IFMAP DRAM BW',' Avg FILTER DRAM BW', ' Avg OFMAP DRAM BW']].values.tolist()  
        results_extracted2 = results_extracted2[0]
        df3 = pd.read_csv(run_results / name / "DETAILED_ACCESS_REPORT.csv")
        results_extracted3 = df3[[' DRAM IFMAP Reads',' DRAM Filter Reads']].values.tolist()  
        results_extracted3 = results_extracted3[0]
        mode = [item]
        data3 = data2.copy()
        data3.extend(total_cycles)
        data3.extend(mode)
        data3.extend(results_extracted2)
        data3.extend(results_extracted3)
        writer2.writerow(data3)

results.close()
results2.close()