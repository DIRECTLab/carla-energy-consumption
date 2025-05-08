# World Creation Notes
## Current Method
1. Go to the URL `https://www.openstreetmap.org/export#map=17/40.770154/-111.891686` to open up OpenStreetMap in SLC,UT
2. Select the `manually select a different area` to snip the area that you want to export in an .osm file.
3. Rename the .osm file in downloads
4. In the terminal go to your `PythonAPI/util` directory and run this command: `python3 osm_to_xodr.py -i ../../../Downloads/<filename>.osm -o ../../Import/<filename>.xodr --traffic-lights`. This will use a python script that will convert an .osm file into a .xodr which is half of what the UE4 needs to build the map. 
5. Open up Blender, and select the Blosm tool. Import your .osm file. I'm still figuring out fully what to do here to make everything look good, but for now just export this into the `carla/Import` as a .fbx file. 
6. Run `make import` in the `carla` directory. This is what makes the map.
7. Run `make launch` and your map should appear in the content browser under `map_package/Maps/<filename>`
8. In order to make the ego vehicle populate in the world, you have to update all 129 spawning points to be on land
9. To add landscape quickly, use the landscape mode in the `modes` on the top bar of the UE. This URL is super helpful to know what parameters you should put for your landscape `https://dev.epicgames.com/documentation/en-us/unreal-engine/creating-landscapes?application_version=4.27`
10. I figured out how to add the weather by comparing the inputs for Town10 under `BP_Sky` and this CARLA Document `https://dev.epicgames.com/documentation/en-us/unreal-engine/creating-landscapes?application_version=4.27`

## Things To Do
2. Figure out the best way to not have roads just dying or if I need to change that at all
2. Fix the graphics
3. Add traffic controls
3. Figure out the correct coordinates to upload the charging pads
4. Add weather conditions
5. Add NPC's 


## Using Driving Scenario Creator
### Videos/Links
* [Map Your World: Using Open Source Tools in Blender for CARLA Simulator](https://www.youtube.com/watch?v=5QLc27o7zhc)
* Use this link to get the Driving Scenario Creator: [Blender-Driving-Scenario-Creator](https://github.com/johschmitz/blender-driving-scenario-creator/releases?page=1)

### Fixes
If you can't install the Driving_Scenario_Creator.zip file and Blender talks about not having scenariogeneration, lxml, numpy, scipy then you are going to have to uninstall them one by one using the Blender's Python and then install them using the Blender's Python. It's a headache and a half, but Chat was super helpful getting the correct commands. Here are a couple that I used to uninstall and reinstall:
```bash
./python3.11 -m pip uninstall lxml #uninstalls from Blender's python

pip uninstall lxml #uninstalls from system python

rm -r /home/carla/blender-4.4.3-linux-x64/4.4/python/lib/python3.11/site-packages/lxml* #Ensures there are no remants of lxml left in blender

ls /home/carla/blender-4.4.3-linux-x64/4.4/python/lib/python3.11/site-packages/lxml #Again, makes sure that lxml no longer exists in blender

./python3.11 -m pip install lxml #installs lxml again into Blender's python
```
I would repeat the process above until I had everything I needed to install the .zip file.

The creator of this tool either dropped an underscore, missed some arguments, or initialized things wrong. These are all of my fixes in order to get his tool to work correctly on Blender 4.4.
* If you get warning errors about missing a parameter when drawing a 4-way junction breaks go to `/home/carla/.config/blender/4.4/scripts/addons/blender-driving-scenario-creator/junction_four_way.py` and adjust `helpers.set_connecting_road_properties(context, 'right', road_contact_point, width_lane_incoming)` to be `helpers.set_connecting_road_properties(context, 'right', road_contact_point, width_lane_incoming, width_lane_incoming)`. We will just assume that the width of the lane coming and leaving are going to be the same width.
* If none of the road tools draw in Driving Scenario Creator.
    1. For me the most common error was Blender couldn't create an instance of DSC_OT_<tool name> to cal lcallback function 'invoke'. If this is the same case for you then you have to change these files:
        * road_straight.py
        * road_arc.py
        * road_clothoid.py
        * road_clothoid_triple.py
        * road_parametric_polynomial.py
    2. The fix you have to implement is first commenting out (using road-clothoid.py as an example):
        ```python
            def __init__(self):
               self.geometry = DSC_geometry_clothoid()
        ```
        and add this instead:
        ```python
            def invoke(self, context, event):
                self.geometry = DSC_geometry_clothoid()
                return super().invoke(context, event)
        ```