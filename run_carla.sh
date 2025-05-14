#!/bin/bash
#I made some edits to this script to start getting our extension working with carla unreal engine 5
eval "$(conda shell.bash hook)"

if conda env list | grep -qw "client-carlaUE5"; then
  echo "Carla client conda env exists, skipping installation..."
  conda activate client-carlaUE5
else
  echo "Carla conda env client-carlaUE5 does not exist, installing..."
  conda create -n client-carlaUE5 python=3.11.8 -y
  conda activate client-carlaUE5
  conda install -c conda-forge pandas matplotlib pygame shapely networkx -y
  pip install /home/carla/CarlaUE5/Build/PythonAPI/dist/carla-0.10.0-cp311-cp311-linux_x86_64.whl #The new carla version for use with Unreal Engine 5
                                                                                                  #Does not appear on pip, so have to grab it from
                                                                                                  #the local wheel file in the Carla server Build
fi

export RES=$(xrandr | grep '*' | awk '{print $1}')
# export RES="1920x1080"
# export RES="1366x768"
# export RES="1440x900"

python3 manual_control_steeringwheel.py ./input/examples/kenworth.csv -w ./input/examples/Town10_intersection_chargers.csv --res $RES > /dev/null 2>&1 &
python3 navigation/draw_chargers.py ./input/examples/Town10_intersection_chargers.csv