#!/bin/bash
eval "$(conda shell.bash hook)"

show_help() {
  echo "Usage: $0 [-i] [-a] [-v VEHICLE] [-c CHARGERS] [-r RES] [-d] [-h]"
  echo ""
  echo "Options:"
  echo "  -i                Sets up the carlaclient-env then exits"
  echo "  -a                Runs the automated simulation demo. Cannot be combined with "
  echo "                    other options."
  echo "  -v  VEHICLE       Specify name of the vehicle csv to load."
  echo "                       Eg. for tesla.csv enter \"tesla\"."
  echo "  -c  CHARGERS      Specify the name of the csv file with the corresponding map's chargers."
  echo "  -r  WIDTHxHEIGHT  Specify the desired resolution for the client screen. Ie. 1920x1080"
  echo "  -d                Debug Mode. Show all output from commands."
  echo "  -h                Show this help message and exit."
}

# defaults
export RES=$(xrandr | grep '*' | awk 'NR==1 {print $1}')
VEHICLE=kenworth
CHARGERS=Town10_intersection_chargers
DEBUG=false
AUTOMATED_DEMO=false
INSTALL_ONLY=false

# paths relative to this script's location
PATH_TO_CHARGER_OPTIONS="../input/creation"
PATH_TO_INPUT_EXAMPLES="../input/examples"
PATH_TO_MULTITRACKING="../"
PATH_TO_OUTPUT="../output"
PATH_TO_MANUAL_CONTROL="../"
PATH_TO_DRAW_CHARGERS="../navigation"

while getopts "v:c:r:aidh" opt; do
  case $opt in
    v) VEHICLE=$OPTARG ;;
    c) CHARGERS=$OPTARG ;;
    r) RES=$OPTARG ;;
    i) INSTALL_ONLY=true ;;
    a) AUTOMATED_DEMO=true ;;
    d) DEBUG=true ;;
    h) show_help; exit 0 ;;
    *) echo "Invalid option"; exit 1 ;;
  esac
done

setup_conda_env() {
  if conda env list | grep -qw "carlaclient-env"; then
    echo "Carla conda env exists, skipping installation..."
    conda activate carlaclient-env
  else
    echo "Carla conda env does not exist, installing..."
    conda create -n carlaclient-env python=3.8 -y
    conda activate carlaclient-env
    conda install -c conda-forge pandas matplotlib pygame shapely networkx pyautogui opencv -y
    pip install carla==0.9.14
  fi
}

if $INSTALL_ONLY; then
  setup_conda_env
else
  setup_conda_env

  if $AUTOMATED_DEMO; then
    python $PATH_TO_CHARGER_OPTIONS/charger_options.py 2 1 -i 0 \
      --power 100_000 \
      --efficiency 0.95 \
      --seed 0 \
      -m Town10HD > $PATH_TO_INPUT_EXAMPLES/automation-demo-chargers.csv &&

    python $PATH_TO_MULTITRACKING/multitracking.py $PATH_TO_INPUT_EXAMPLES/tracked_agents.csv \
      $PATH_TO_OUTPUT/Town10_lap \
      -w $PATH_TO_INPUT_EXAMPLES/automation-demo-chargers.csv \
      --seed 0 \
      -t 1800\
      -d 0.05
  else
    if $DEBUG; then
      python $PATH_TO_MANUAL_CONTROL/manual_control_steeringwheel.py \
        $PATH_TO_INPUT_EXAMPLES/$VEHICLE.csv \
        -w $PATH_TO_INPUT_EXAMPLES/$CHARGERS.csv \
        --res $RES &
    else
      python $PATH_TO_MANUAL_CONTROL/manual_control_steeringwheel.py \
        $PATH_TO_INPUT_EXAMPLES/$VEHICLE.csv \
        -w $PATH_TO_INPUT_EXAMPLES/$CHARGERS.csv \
        --res $RES > /dev/null 2>&1 &
    fi
  fi

  python $PATH_TO_DRAW_CHARGERS/draw_chargers.py $PATH_TO_INPUT_EXAMPLES/$CHARGERS.csv
fi
