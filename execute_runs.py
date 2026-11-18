from pathlib import Path
import pandas as pd
from math import ceil
from scalesim import scale

arrayHeights = [32,64,128,256]
arrayWidths = [32,64,128,256]
stationary = ["ws", "is", "os"]
work = [512, 1280, 1152] # M,N,K static

arrayHeights = [32]
arrayWidths = [32]
stationary = ["os"]

filename = "results.csv"
results = open(filename,'a+')


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

run_dir = Path('runs_lab')
run_top = Path('topologies_lab') / "partA.csv"
run_layout = Path('layouts/conv_nets') / "test.csv"
run_results = Path('run_results')
for flow in stationary:
    for height in arrayHeights:
        for width in arrayWidths:
            name =  "gemm_"+str(height)+"x"+str(width)+"_"+flow
            name = run_dir / (name + ".cfg")
            run = scale.scalesim(save_disk_space=True, config=name.absolute().as_posix(), topology=run_top.absolute().as_posix(), layout=run_layout.absolute().as_posix(), input_type_gemm=True)
            run.run_scale(top_path='run_results')
            
