# What to do for events

1. open 3 termanal tabs

2. run command to start unreal engine
```bash
~/carla-energy-consumption$ ./run_carla.sh 
Waiting for CarlaUE4 to load... Please do not touch mouse or keyboard
CarlaUE4 is loaded!
Current resolution is: 1920x1080
Waiting for Carla Client to load
pygame window
Carla client is loaded!
```

3. open the CarlaUE4 Editor GUI that just opened and click play

4. start the simulation
```bash
~/carla-energy-consumption$ python3 manual_control_steeringwheel.py ./input/examples/kenworth.csv -w ./input/examples/Town10_intersection_chargers.csv --res 1920x1080
pygame 2.5.2 (SDL 2.28.2, Python 3.8.10)
Hello from the pygame community. https://www.pygame.org/contribute.html
vehicle Name
vehicle
INFO: listening to server 127.0.0.1:2000

Welcome to CARLA manual control with steering wheel Logitech G29.

To drive start by pressing the brake pedal.
Change your wheel_config.ini according to your steering wheel.

To find out the values of your steering wheel use jstest-gtk in Ubuntu.


```

5. populate the map with the chargers
```bash
~/carla-energy-consumption$ python3 navigation/draw_chargers.py ./input/examples/Town10_intersection_chargers.csv 
Waiting for Ctrl-C


```

Everything should be working! Contact Isaac Peterson if you have issues :).
