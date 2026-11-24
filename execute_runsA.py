from pathlib import Path
import pandas as pd
from math import ceil
from scalesim import scale
import csv 

arrayHeights = [32,64,128,256]
arrayWidths = [32,64,128,256]
stationary = ["ws", "is", "os"]
work = [512, 1280, 1152] # M,N,K static

filename = "results.csv"
results = open(filename,'a+')
writer = csv.writer(results)

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

run_dir = Path('runs_labA')
run_top = Path('topologies_lab') / "partA.csv"
run_layout = Path('layouts/conv_nets') / "test.csv"
run_results = Path('run_resultsA')

for flow in stationary:
    for height in arrayHeights:
        for width in arrayWidths:
            name =  "gemm_"+str(height)+"x"+str(width)+"_"+flow
            config_name = run_dir / (name + ".cfg")
            run = scale.scalesim(save_disk_space=True, config=config_name.absolute().as_posix(), topology=run_top.absolute().as_posix(), layout=run_layout.absolute().as_posix(), input_type_gemm=True)
            run.run_scale(top_path='run_resultsA')

            data = ["gemm", name, flow, height, width, height*width, predict_total_cycles(height, width, flow)]    

            df = pd.read_csv(run_results / name / "COMPUTE_REPORT.csv")
            results_extracted = df[[' Total Cycles', ' Stall Cycles', ' Overall Util %', ' Mapping Efficiency %']].values.tolist()    
            results_extracted = results_extracted[0]    
            data.extend(results_extracted)
            writer.writerow(data)

results.close()