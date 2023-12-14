"""
Data for these plots was generated using the command
```
python multitracking.py input/tracked_agents.csv output/Town06_lap -w input/Town06_intersection_chargers.csv --seed 0 -t 230 -d 0.05 -m Town06
```
"""


import os
import matplotlib.pyplot as plt
import pandas as pd


dataPath = "output/Town06_lap/"
vehicles = pd.read_csv(os.path.join(dataPath, "vehicles.csv"), index_col=0)
vId = vehicles.index[0]
vInfo = pd.read_csv(os.path.join(dataPath, f"vehicle{vId}.csv"), index_col=0)
vInfo.rename(columns={
    # 'time': 'Time (s)',
    'speed': 'Speed (m/s)', 
    'acceleration': 'Acceleration (m/s^2)', 
    'power_consumed': 'Power Consumed (W)', 
    'charge_power': 'Charge Power (W)', 
    'SOC': 'State of Charge',
}, inplace=True)
vInfo['Elapsed Time (s)'] = vInfo['time'] - vInfo['time'].min()

attrs = (
    # 'Speed (m/s)', 
    # 'Acceleration (m/s^2)', 
    'Power Consumed (W)', 
    'Charge Power (W)', 
    'State of Charge'
)

fig, axs = plt.subplots(len(attrs), layout='constrained')
for attr, ax in zip(attrs, axs):
    vInfo.plot('Elapsed Time (s)', attr, ax=ax, legend=False, ylabel=attr)
plt.show()

end = 50
vInfoSlice = vInfo[(vInfo['Elapsed Time (s)'] <= end)]

fig, axs = plt.subplots(len(attrs), layout='constrained')
for attr, ax in zip(attrs, axs):
    vInfoSlice.plot('Elapsed Time (s)', attr, ax=ax, legend=False, ylabel=attr)
plt.show()

fig, axs = plt.subplots(2, layout='constrained')
vInfoSlice.plot('Elapsed Time (s)', 'Power Consumed (W)', ax=axs[0])
vInfoSlice.plot('Elapsed Time (s)', 'Charge Power (W)', ax=axs[0])
vInfoSlice.plot('Elapsed Time (s)', 'State of Charge', ax=axs[1])
plt.show()
