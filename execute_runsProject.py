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
layout = Path('layouts/conv_nets') / 'test.csv'
layout = layout.absolute().as_posix()

def run_scalesim(panelSize, matrixSize, isFirstRound):
    loadADelay = matrixSize * panelSize / (bandwidth if isFirstRound else linkBandwidth) # if first chiplet, then reads panel of A from DRAM; else, read panel from ring neighbor using ring link
    loadBDelay = hopDelay + alpha + panelSize * matrixSize / 16 / bandwidth # load from DRAM
    # C is stored at end of all computation
    
    name = str(matrixSize)+"_"+str(panelSize)
    path = name / ".csv"
    config = configs / 'project_exploration.cfg'
    
    run = scale.scalesim(save_disk_space=True, config=path.absolute().as_posix(), topology=config.absolute().as_posix(), layout=layout.absolute().as_posix(), input_type_gemm=True)
    run.run_scale(top_path='run_results_project')

    