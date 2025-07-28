Getting chargers on specific roads and lanes is a bit complicated and tricky because for some reason unreal doesnt recognize our roads coordinates and using actors to spawn on certain roads spawns chargers at diffefrent locations than expected, so I came up with this technique though long but works. 

1. Run the server and move the viewer/screen to the junction whose lane you want to place the chargers. 
2. Run the [junction_chargers.py](./junction_chargers.py) script and change the interval to like 2.0 seconds or a time frame you think would be convenient to view the charger spawn at that junction and also the csv file related to it.
3. Run the csv file at the [run_carla.sh](../../run_carla.sh) and manually delete each coordinate until you get the charger that lies directly on the lane you want the charger on. 
4. Run the [propagate_chargers.py](./propagate_chargers.py) script and pass the csv file that conatains the head chrger you want to populate from 


## HOW TO RUN roadslanes_chargers.py
usage: `propagate_chargers.py [-h] [--separate] [-n N] [-i I] [-m MAP] [--host H] [--port P] init_chargers outfile d`
eg. `python propagate_chargers.py /home/directlab/carla-energy-consumption/initial.csv -i 0 -n 10 final.csv 4.0`

- this runs the script and reads coordinates of the charger you want to populate from from the `initial.csv`. Interval (-i) is set to 0 to make demonstrations active; -n 10 generates 10 chargers and ouputs the coorinates to `final.csv`; d = 4.0 is the distance after each charger to propagate. If you want your chargers to be end-to-end, make sure `d` is the same length of your initial charger.