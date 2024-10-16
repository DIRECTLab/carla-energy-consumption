#!/bin/bash

cd ~/carla 
make launch > /dev/null 2>&1 &  

echo "Waiting for CarlaUE4 to load... Please do not touch mouse or keyboard"

while true; do
    if wmctrl -l | grep -q "Unreal Editor"; then
        active_window=$(xdotool getactivewindow getwindowname)

        if [[ "$active_window" == *"CarlaUE4"* ]]; then
            echo "CarlaUE4 is loaded!"
            break
        fi
    fi
    sleep 1  
done

wmctrl -a "CarlaUE4"
sleep 1 

xdotool key Alt+p 

sleep 10 

export RES=$(xrandr | grep '*' | awk '{print $1}')
echo "Current resolution is: $RES"

cd ~/carla-energy-consumption
python3 manual_control_steeringwheel.py ./input/examples/kenworth.csv -w ./input/examples/Town10_intersection_chargers.csv --res $RES > /dev/null 2>&1 &
python3 navigation/draw_chargers.py ./input/examples/Town10_intersection_chargers.csv > /dev/null 2>&1 &

echo "Waiting for Carla Client to load"

while true; do
    if wmctrl -l | grep -q "pygame"; then
        active_window=$(xdotool getactivewindow getwindowname)
        echo $active_window

        if [[ "$active_window" == *"pygame"* ]]; then
            echo "Carla client is loaded!"
            break
        fi
    fi
    sleep 1  
done

wmctrl -a "pygame"



