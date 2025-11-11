#!/bin/bash
eval "$(conda shell.bash hook)"

show_help() {
  echo "Usage: $0 [-v VEHICLE] [-r RES] [-h]"
  echo ""
  echo "Options:"
  echo "  -a                Runs the automated simulation demo. Cannot be combined with "
  echo "                    other options."
  echo "  -v  VEHICLE       Specify name of the vehicle csv to load."
  echo "                       Eg. for tesla.csv enter \"tesla\"."
  echo "  -c  CHARGERS      Specify the name of the csv file with the corresponding map's chargers."
  echo "  -r  WIDTHxHEIGHT  Specify the desired resolution for the client screen. Ie. 1920x1080"
  echo "  -d                Debug Mode. Show all output from commands."
  echo "  -h                Show this help message and exit."
}

export RES=$(xrandr | grep '*' | awk 'NR==1 {print $1}')
VEHICLE=kenworth
CHARGERS=Town10_intersection_chargers
DEBUG=false
AUTOMATED_DEMO=false

while getopts "v:c:s:r:adh" opt; do
  case $opt in
    v) VEHICLE=$OPTARG ;;
    c) CHARGERS=$OPTARG ;;
    r) RES=$OPTARG ;;
    a) AUTOMATED_DEMO=true ;;
    d) DEBUG=true ;;
    h) show_help; exit 0 ;;
    *) echo "Invalid option"; exit 1 ;;
  esac
done

if conda env list | grep -qw "carla-client-env"; then
  echo "Carla conda env exists, skipping installation..."
  conda activate carla-client-env
else
  echo "Carla conda env does not exist, installing..."
  conda create -n carla-client-env python=3.8 -y
  conda activate carla-client-env
  conda install -c conda-forge pandas matplotlib pygame shapely networkx -y
  pip install carla==0.9.14
fi

if $AUTOMATED_DEMO; then
  python input/creation/charger_options.py 2 1 -i 0 \
    --power 100_000 \
    --efficiency 0.95 \
    --seed 0 \
    -m Town10HD > input/examples/automation-demo-chargers.csv &&

  python multitracking.py input/examples/tracked_agents.csv \
    output/Town10_lap \
    -w input/examples/automation-demo-chargers.csv \
    --seed 0 \
    -t 230 \
    -d 0.05
else
  if $DEBUG; then
    python manual_control_steeringwheel.py \
      ./input/examples/$VEHICLE.csv \
      -w ./input/examples/$CHARGERS.csv \
      --res $RES &
  else
    python manual_control_steeringwheel.py \
      ./input/examples/$VEHICLE.csv \
      -w ./input/examples/$CHARGERS.csv \
      --res $RES > /dev/null 2>&1 &
  fi
fi

python navigation/draw_chargers.py ./input/examples/$CHARGERS.csv
