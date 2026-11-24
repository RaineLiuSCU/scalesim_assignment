from pathlib import Path
import pandas as pd
from math import ceil
from scalesim import scale
import csv 
import configparser
import ProcessOptimizer as po

dataflow = "os"
mode = "USER"
work = [512, 1280, 1152] # M,N,K static

filename = "results_b.csv"
results = open(filename,'a+', newline='')
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

run_dir = Path('runs_labB')
run_top = Path('topologies_lab') / "partA.csv"
run_layout = Path('layouts/conv_nets') / "test.csv"
run_results = Path('run_resultsB')

def run_scalesim(inputs): #input list: height, width, ifmap, filter, ofmap
    if(len(inputs) != 5):
        print("input format incorrect. ")
        return -1
    # must modify height, width, sram sizes so they are multiples of 8 and powers of 2 respectively
    height = inputs[0] * 8
    width = inputs[1] * 8
    ifmap = 2 ** inputs[2]
    filter = 2 ** inputs[3]
    ofmap = 2 ** inputs[4]
    if (height*width + 3.25 * (ifmap+filter+ofmap) > 16384):
        return 80000000
    
    config_override = configparser.ConfigParser()
    config_override.read("configs/google.cfg")
    name = "BO_gemmB_"+str(height)+"_"+str(width)+"_"+str(ifmap)+"_"+str(filter)+"_"+str(ofmap)+"_"+mode
    config_override['architecture_presets'].update({"ArrayHeight": str(height), 
                                                            "ArrayWidth": str(width), 
                                                            "Dataflow": dataflow,
                                                            "IfmapSramSzkB": str(ifmap),
                                                            "FilterSramSzkB": str(filter),
                                                            "OfmapSramSzkB": str(ofmap)})
    config_override['run_presets'].update({"InterfaceBandwidth": "USER"})
    config_override['general'].update({"run_name": name})
    config_override["architecture_presets"].update({"Bandwidth": str(50)})
    config_override["layout"].update({"IfmapSRAMBankBandwidth": str(50),"FilterSRAMBankBandwidth": str(50)})
    config_path = run_dir / (name + ".cfg")
    new_config = open(config_path, "w")
    config_override.write(new_config)
    new_config.close()

    run = scale.scalesim(save_disk_space=True, config=config_path.absolute().as_posix(), topology=run_top.absolute().as_posix(), layout=run_layout.absolute().as_posix(), input_type_gemm=True)
    run.run_scale(top_path='run_resultsB')

    data = ["gemm", name, "os", height, width, height*width, predict_total_cycles(height, width, "os")]    

    df = pd.read_csv(run_results / name / "COMPUTE_REPORT.csv")
    results_extracted = df[[' Total Cycles', ' Stall Cycles', ' Overall Util %', ' Mapping Efficiency %']].values.tolist()    
    total_cycles = df[[' Total Cycles (incl. prefetch)']].values.tolist()
    total_cycles = total_cycles[0]
    results_extracted = results_extracted[0]  

    data2 = [ifmap, filter, ofmap]

    data.extend(results_extracted)
    data.extend(data2)
    data.extend(total_cycles)
    data.append("USER")
    writer.writerow(data)

    return total_cycles[0]

# run_scalesim([13,18,7,7,7]) # test with array shape 104, 144, 128, 128, 128

height_space = po.Integer(4,15, name="Array height / 8")
width_space = po.Integer(4,15, name="Array width / 8")
ifmap_space = po.Integer(5,13, name="log2(ifmap SRAM size)")
filter_space = po.Integer(5,13, name="log2(filter SRAM size)")
ofmap_space = po.Integer(5,13, name="log2(ofmap SRAM size)")

SPACE = po.Space([height_space, width_space, ifmap_space, filter_space, ofmap_space])
opt = po.Optimizer(SPACE, base_estimator = "GP", n_initial_points = 6, lhs = True)
res = ""
scalesim_runs = 0
min_cycles = 80000000
min_inputs = []
cycle_history = []
while scalesim_runs < 27:
    new_inputs = opt.ask()
    total_cycles = run_scalesim(new_inputs)
    res = opt.tell(new_inputs, total_cycles)
    if total_cycles != 80000000:
        scalesim_runs = scalesim_runs + 1
        cycle_history.append(total_cycles)
    if total_cycles < min_cycles:
        min_cycles = total_cycles
        min_inputs = new_inputs

po.plot_convergence(res)
results.close()

cycles = open("B2history.csv", 'w')
writer = csv.writer(cycles)
writer.writerow(cycle_history)
writer.writerow([min_cycles])
writer.writerow(min_inputs)
cycles.close()