#!/bin/bash
eval "$(conda shell.bash hook)"

show_help() {
  echo "Usage: $0 [-v VEHICLE] [-r RES] [-h]"
  echo ""
  echo "Leave with no options to use defaults"
  echo ""
  echo "Options:"
  echo "  -v  VEHICLE Specify name of the vehicle csv to load. Ie. for kenworth.csv, enter kenworth."
  echo "  -r  RES Specify the desired resolution for the client screen. Ie. 1920x1080"
  echo "  -h  Show this help message and exit."
}

#Default values
export RES=$(xrandr | grep '*' | awk '{print $1}')
VEHICLE=lincoln

#Handles the options
while getopts "v:s:r:h" opt; do
  case $opt in
    v) VEHICLE=$OPTARG ;;
    r) RES=$OPTARG ;;
    h) show_help; exit 0 ;;
    *) echo "Invalid option"; exit 1 ;;
  esac
done

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

python3 manual_control_steeringwheel.py ./input/examples/$VEHICLE.csv -w ./input/examples/Town10_intersection_chargers.csv --res $RES > /dev/null 2>&1 &
python3 navigation/draw_chargers.py ./input/examples/Town10_intersection_chargers.csv