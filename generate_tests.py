import configparser
from pathlib import Path
import pandas as pd
from math import ceil
from scalesim import scale
import os 

arrayHeights = [32,64,128,256]
arrayWidths = [32,64,128,256]
stationary = ["ws", "is", "os"]

# arrayHeights = [32]
# arrayWidths = [32]
# stationary = ["os"]

config_override = configparser.ConfigParser()
config_override.read("configs/google.cfg")

run_dir = Path('runs_lab')
run_top = Path('topologies_lab') / "partA.csv"
run_layout = Path('layouts/conv_nets') / "test.csv"

for flow in stationary:
    for height in arrayHeights:
        for width in arrayWidths:
            config_override['architecture_presets'].update({"ArrayHeight": str(height), "ArrayWidth": str(width), "Dataflow": flow})
            config_override['run_presets'].update({"InterfaceBandwidth": "CALC"})
            config_override['general'].update({"run_name": name})
            name = run_dir / (name + ".cfg")
            new_config = open(name, "w")
            config_override.write(new_config)
