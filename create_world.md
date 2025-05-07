# Notes
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