import configparser
from pathlib import Path
import pandas as pd
from math import ceil
from scalesim import scale
import csv

arrayHeight = 64
arrayWidth = 64

arrayHeightBaseline = 256
arrayWidthBaseline = 256
bandwidth = 1024

panelSize = [64,256,1024]
matrixSize = [4096, 8192]
csv_header = ['Layer','M','N','K',]
isBaseline = [False, True]
mode = 'CALC'

topologies = Path('topologies_project')
configs = Path('runs_project')

config_override = configparser.ConfigParser()
config_override.read("configs/google.cfg")

# generate topologies
for i in matrixSize:
    for j in panelSize:
        for k in isBaseline:
            M = i
            K = j
            N = i if k else ceil(i/16)
            name = str(M) + "_" + str(N) + "_" + str(K)
            path = name + ".csv"

            f = open(topologies / path, 'w')
            writer = csv.writer(f)
            writer.writerow(csv_header)

            layerName = 'gemm_' + name
            csv_row = [layerName, M, N, K,]
            writer.writerow(csv_row)
            f.close()

            config_override['architecture_presets'].update({"ArrayHeight": str(256 if k else 64), 
                                                        "ArrayWidth": str(256 if k else 64), 
                                                        "Dataflow": str('os'),
                                                        "Bandwidth": str(bandwidth),
                                                })
            config_override['run_presets'].update({"InterfaceBandwidth": mode})
            config_override['general'].update({"run_name": name})
            name = configs / (name + ".cfg")
            new_config = open(name, "w")
            config_override.write(new_config)

# generate ring array config


# #generate baseline array config 
# config_override['architecture_presets'].update({"ArrayHeight": '256', "ArrayWidth": '256'})
# baseline = configs / ("project_baseline.cfg")
# new_config = open(baseline, "w")
# config_override.write(new_config)
