#!/bin/bash
eval "$(conda shell.bash hook)"

if conda env list | grep -qw "carlaenv"; then
  echo "Carla conda env exists, skipping installation..."
  conda activate carlaenv
else
  echo "Carla conda env does not exist, installing..."
  conda create -n carlaenv python=3.8 -y
  conda activate carlaenv
  conda install -c conda-forge pandas matplotlib pygame shapely networkx -y
  pip install carla==0.9.14
fi

export RES=$(xrandr | grep '*' | awk 'NR==1 {print $1}')
python3 manual_control_steeringwheel.py --host 129.123.153.74 ./input/examples/ogdenbus.csv -w ./input/examples/Town10_intersection_chargers.csv --res $RES > /dev/null 2>&1 &
python3 navigation/draw_chargers.py --host 129.123.153.74 ./input/examples/Town10_intersection_chargers.csv



# Wi-Fi IP Address: 144.39.45.43
# Ethernet IP Address: 129.123.153.74 

