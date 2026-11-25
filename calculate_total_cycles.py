import pandas as pd
from math import ceil

df = pd.read_csv('results_project.csv')
df.reset_index()

computeList = df['Total Cycles'].to_numpy().ravel()
arrayHeight = 64
arrayWidth = 64
arrayHeightBaseline = 256
arrayWidthBaseline = 256
bandwidth = 1024
linkBandwidth = 32
hopDelay = 20
DRAM_alpha = 500
link_alpha = 500
panelSize = [64,256,1024]
matrixSize = [4096, 8192]
isBaseline = [False, True]

panelList = []
AReadsList = []
BReadsList = []
ringTransferList = []
CWriteList = []
cyclesPerGEMMList = []
isBaselineList = []
sizeList = []
index = 0

for i in matrixSize:
    for j in panelSize:
        for k in isBaseline:
            width = arrayWidthBaseline if k else arrayWidth
            n = i if isBaseline else ceil(i/16)
            panels = i // j
            steps = panels + arrayWidth - 1 

            AReads = panels * (DRAM_alpha + i * j / bandwidth) # each panel is read only once
            BReads = steps * DRAM_alpha + (width * panels) * (j * n) / bandwidth #each chiplet reads b x n/16 if is not baseline; each chiplet reads B (# panel) times
            ringTransfer = (steps - 1) * (hopDelay + link_alpha + i * j / linkBandwidth)
            compute = steps * computeList[index]
            CWrite = DRAM_alpha + i ** 2 / bandwidth # C is written to DRAM at end of round
            cyclesPerGEMM = AReads + BReads + ringTransfer + compute + CWrite

            sizeList.append(i)
            panelList.append(j)
            isBaselineList.append(k)
            
            AReadsList.append(AReads)
            BReadsList.append(BReads)
            ringTransferList.append(ringTransfer)
            CWriteList.append(CWrite)
            cyclesPerGEMMList.append(cyclesPerGEMM)

            index = index + 1

addenum = {'Matrix Size': sizeList, 'Panel Size': panelList, 'Is Baseline?': isBaselineList, 'A Reads': AReadsList, 'B Reads': BReadsList, 'Ring Transfer': ringTransferList, 'C Write': CWriteList, 'Cycles Per GEMM': cyclesPerGEMMList}
df = pd.concat([df, pd.DataFrame(data=addenum)], axis=1)
df = df.drop(columns=['Unnamed: 0'])
df.to_csv("results_project_total.csv")


