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
csv_header = ['Layer','M','N','K',]
mode = 'CALC'

topologies = Path('topologies_project')
configs = Path('runs_project')
results = Path('run_results_project')
layout = Path('layouts/conv_nets') / 'test.csv'
layout = layout.absolute().as_posix()

def run_scalesim(panelSize, matrixSize, isBaseline):
    linkDelay = hopDelay + alpha + matrixSize * panelSize / linkBandwidth # each ring link takes this long to transfer panel to neighbor
    if(isBaseline):
        panelSize = matrixSize
        linkDelay = 0 # baseline has no neighbors to pass to
    dramDelay = (matrixSize * panelSize + panelSize * matrixSize) / bandwidth  # total read words across A and B, divided by shared bandwidth
    
    writeDelay = matrixSize ** 2 / bandwidth # C is written to DRAM at end of round
    
    name = str(matrixSize)+"_"+str(panelSize)
    topology = name / ".csv"
    config = configs / ('project_baseline.cfg' if isBaseline else 'project_exploration.cfg')
    
    run = scale.scalesim(save_disk_space=True, config=config.absolute().as_posix(), topology=topology.absolute().as_posix(), layout=layout.absolute().as_posix(), input_type_gemm=True)
    run.run_scale(top_path='run_results_project')

    df = pd.read_csv(results / name / "COMPUTE_REPORT.csv")
    results_extracted = df[[' Total Cycles', ' Stall Cycles', ' Overall Util %', ' Mapping Efficiency %']]
    results_extracted['Name'] = [name]
    results_extracted['DRAM Delay'] = [dramDelay]
    results_extracted['Link Delay'] = [linkDelay]
    results_extracted['Write Delay'] = [writeDelay]
    results_extracted['Cycles Per Round'] = [dramDelay + linkDelay + writeDelay + results_extracted[' Total Cycles'].values(0)]
    return results_extracted

