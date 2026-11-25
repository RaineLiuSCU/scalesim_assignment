from pathlib import Path
import pandas as pd
from math import ceil
from scalesim import scale
import csv 

arrayHeight = 64
arrayWidth = 64
numPEs = 16
arrayHeightBaseline = 256
arrayWidthBaseline = 256
bandwidth = 1024
linkBandwidth = 32
hopDelay = 20
alphaDRAM = 500
linkDRAM = 500
panelSize = [64,256,1024]
matrixSize = [4096, 8192]
isBaseline = [False, True]

topologies = Path('topologies_project')
configs = Path('runs_project')
results = Path('run_results_project')
layout = Path('layouts/conv_nets') / 'test.csv'

def run_scalesim(panelSize, matrixSize, isBaseline):

    # determine workload; varies on whether is baseline or not
    name = (str(matrixSize)+"_"+ str(matrixSize) + "_" +str(panelSize)) if isBaseline else (str(matrixSize)+"_"+ str(ceil(matrixSize/16)) + "_" +str(panelSize))
    topology = topologies / (name + ".csv")
    config = configs / (name + ".cfg")
    
    run = scale.scalesim(save_disk_space=True, config=config.absolute().as_posix(), topology=topology.absolute().as_posix(), layout=layout.absolute().as_posix(), input_type_gemm=True)
    run.run_scale(top_path='run_results_project')

    df = pd.read_csv(results / name / "COMPUTE_REPORT.csv")
    results_extracted = df[[' Total Cycles', ' Overall Util %', ' Mapping Efficiency %']]
    results_extracted['Name'] = [name]
    results_extracted['Is Baseline?'] = [isBaseline]
    results_extracted = results_extracted.rename(columns={' Total Cycles': 'Total Cycles', ' Overall Util %': 'Overall Util %', ' Mapping Efficiency %': 'Mapping Efficiency %'})
    results_extracted = results_extracted[['Name', 'Total Cycles', 'Overall Util %', 'Mapping Efficiency %']]
    return results_extracted

df = pd.DataFrame(columns=['Name', 'Total Cycles', 'Overall Util %', 'Mapping Efficiency %'])
for i in matrixSize:
    for j in panelSize:
        for k in isBaseline:
            per_run = run_scalesim(j, i, k)
            df = pd.concat([df, per_run])

df.to_csv('results_project_scalesim.csv')