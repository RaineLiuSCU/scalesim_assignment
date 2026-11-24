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
alpha = 500

panelSize = [64,256,1024]
matrixSize = [4096, 8192]
csv_header = ['Layer','M','N','K',]
mode = 'CALC'

topologies = Path('topologies_project')
configs = Path('runs_project')

def run_scalesim(panelSize, matrixSize, isFirstRound):
    loadADelay = matrixSize * panelSize / (bandwidth/numPEs if isFirstRound else linkBandwidth) # if first chiplet, then reads panel of A from DRAM; else, read panel from ring neighbor using ring link
    loadBDelay = alpha + panelSize * matrixSize / 16 / bandwidth
    storeDelay = matrixSize ** 2 / 16 