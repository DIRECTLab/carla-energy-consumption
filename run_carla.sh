#!/bin/bash
eval "$(conda shell.bash hook)"


show_help() {
  echo "Usage: $0 [-v VEHICLE] [-r RES] [-h]"
  echo ""
  echo "Options:"
  echo "  -v  VEHICLE       Specify name of the vehicle csv to load. Ie. for kenworth.csv, enter kenworth."
  echo "  -c  CHARGERS      Specify the name of the csv file with the corresponding map's chargers."
  echo "  -r  WIDTHxHEIGHT  Specify the desired resolution for the client screen. Ie. 1920x1080"
  echo "  -d                Debug Mode. Show all output from commands."
  echo "  -h                Show this help message and exit."
}

#Default values
#NR is which monitor's resolution to start pygame with, 1 is the primary monitor.
export RES=$(xrandr | grep '*' | awk 'NR==1 {print $1}')
VEHICLE=tesla
CHARGERS=Town10_intersection_chargers
DEBUG=false

#Handles the options
while getopts "v:c:s:r:dh" opt; do
  case $opt in
    v) VEHICLE=$OPTARG ;;
    c) CHARGERS=$OPTARG ;;
    r) RES=$OPTARG ;;
    d) DEBUG=true ;;
    h) show_help; exit 0 ;;
    *) echo "Invalid option"; exit 1 ;;
  esac
done

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

if $DEBUG; then
  python3 manual_control_steeringwheel.py ./input/examples/$VEHICLE.csv -w ./input/examples/$CHARGERS.csv --res $RES;
else
  python3 manual_control_steeringwheel.py ./input/examples/$VEHICLE.csv -w ./input/examples/$CHARGERS.csv --res $RES > /dev/null 2>&1 &
fi

python3 navigation/draw_chargers.py ./input/examples/$CHARGERS.csv

# Wi-Fi IP Address: 144.39.45.43
# Ethernet IP Address: 129.123.153.74 

