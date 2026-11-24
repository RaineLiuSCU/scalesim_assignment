import configparser
from pathlib import Path
import pandas as pd
from math import ceil
from scalesim import scale
import os 

arrayHeight = [128, 104, 88]
arrayWidth = [120, 144, 72]
stationary = "os"
IfmapSramSzkB = [32, 128, 1024]
FilterSramSzkB = [32, 128, 1024]
OfmapSramSzkB = [32, 128, 1024]
mode =["USER", "CALC"]

config_override = configparser.ConfigParser()
config_override.read("configs/google.cfg")

run_dir = Path('runs_labB')
run_top = Path('topologies_lab') / "partA.csv"
run_layout = Path('layouts/conv_nets') / "test.csv"

for item in mode:
    for i in range(3):
        name = "gemmB_"+str(arrayHeight[i])+"_"+str(arrayWidth[i])+"_"+str(IfmapSramSzkB[i])+"_"+str(FilterSramSzkB[i])+"_"+str(OfmapSramSzkB[i])+"_"+item
        config_override['architecture_presets'].update({"ArrayHeight": str(arrayHeight[i]), 
                                                        "ArrayWidth": str(arrayWidth[i]), 
                                                        "Dataflow": str(stationary),
                                                        "IfmapSramSzkB": str(IfmapSramSzkB[i]),
                                                        "FilterSramSzkB": str(FilterSramSzkB[i]),
                                                        "OfmapSramSzkB": str(OfmapSramSzkB[i])})
        
        config_override['run_presets'].update({"InterfaceBandwidth": item})
        config_override['general'].update({"run_name": name})
        config_override["architecture_presets"].update({"Bandwidth": str(50)})
        config_override["layout"].update({"IfmapSRAMBankBandwidth": str(50),"FilterSRAMBankBandwidth": str(50)})
        name = run_dir / (name + ".cfg")
        new_config = open(name, "w")
        config_override.write(new_config)
