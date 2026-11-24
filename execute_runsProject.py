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
alpha = 500

panelSize = [64,256,1024]
matrixSize = [4096, 8192]
isBaseline = [False, True]

topologies = Path('topologies_project')
configs = Path('runs_project')
results = Path('run_results_project')
layout = Path('layouts/conv_nets') / 'test.csv'

def run_scalesim(panelSize, matrixSize, isBaseline):
    linkDelay = hopDelay + alpha + matrixSize * panelSize / linkBandwidth # each ring link takes this long to transfer panel to neighbor
    if(isBaseline):
        linkDelay = 0 # baseline has no neighbors to pass to
    dramDelay = (matrixSize * panelSize + panelSize * matrixSize) / bandwidth  # total read words across A and B, divided by shared bandwidth
    
    writeDelay = matrixSize ** 2 / bandwidth # C is written to DRAM at end of round

    # determine workload; varies on whether is baseline or not
    name = (str(matrixSize)+"_"+ str(matrixSize) + "_" +str(panelSize)) if isBaseline else (str(matrixSize)+"_"+ str(ceil(matrixSize/16)) + "_" +str(panelSize))
    topology = topologies / (name + ".csv")
    config = configs / (name + ".cfg")
    
    run = scale.scalesim(save_disk_space=True, config=config.absolute().as_posix(), topology=topology.absolute().as_posix(), layout=layout.absolute().as_posix(), input_type_gemm=True)
    run.run_scale(top_path='run_results_project')

    df = pd.read_csv(results / name / "COMPUTE_REPORT.csv")
    results_extracted = df[[' Total Cycles', ' Overall Util %', ' Mapping Efficiency %']]
    results_extracted['Name'] = [name]
    results_extracted['DRAM Delay'] = [dramDelay]
    results_extracted['Link Delay'] = [linkDelay]
    results_extracted['Write Delay'] = [writeDelay]
    results_extracted['Cycles Per Round'] = [dramDelay + linkDelay + writeDelay + results_extracted[' Total Cycles'].values[0]]
    results_extracted['Is Baseline?'] = [isBaseline]
    results_extracted = results_extracted.rename(columns={' Total Cycles': 'Total Cycles', ' Overall Util %': 'Overall Util %', ' Mapping Efficiency %': 'Mapping Efficiency %'})
    results_extracted = results_extracted[['Name', 'Cycles Per Round', 'DRAM Delay', 'Link Delay', 'Write Delay', 'Total Cycles', 'Overall Util %', 'Mapping Efficiency %']]
    return results_extracted

df = pd.DataFrame(columns=['Name', 'Cycles Per Round', 'DRAM Delay', 'Link Delay', 'Write Delay', 'Total Cycles', 'Overall Util %', 'Mapping Efficiency %'])
for i in matrixSize:
    for j in panelSize:
        for k in isBaseline:
            per_run = run_scalesim(j, i, k)
            df = pd.concat([df, per_run])

df.to_csv('results_project.csv')