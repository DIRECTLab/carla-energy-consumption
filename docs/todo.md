# Current todos for the project

## In Progress


## Backlog

1. [] Write up in the docs or notes how the desktop shortcut works so next guy can figure it out should there be issues.
1. [] Is there a more robust way than expiicitly putting the path to UE4 in the server script to get the desktop shortcut start way working? Thinking about setting this up on other machines than just the one carla machine.
1. [] Clean up the demo files themselves now that things are working to be more optimized
1. [] Update [roadlanes_README.md](../input/creation/roadlanes_README.md) to match new ways of running carla
1. [] Update [add_new_vehicle.md](./add_new_vehicle.md) to match the new ways of running carla 

## Completed

1. [x] Get Carla demo able to run from desktop icon
    * Desktop shortcut is kind of working, but crashing for some reason when running the stuff, see the output log I made in the home directory, should show the errors that are occuring and how to fix
1. [x] Make sure docs are updated to reflect the new way to run carla
1. [x] Clean up the scripts so all paths work and the layout is more intuitive with the addition of the new script/way to run carla
1. [x] move the `notes` directory into the docs folder, and cleanup links as needed
1. [x] rename the various demo files to have a more intuitive naming system
1. [x] refactor the `run_carla_demo.sh` script to make demos even easier
    * [x] Start with kenworth as default
    * [x] to be able to run the manual and/or the automated demo

## Things To Do (these were in [create_world.md](./create_world.md))

1. [] Figure out the best way to not have roads just dying or if I need to change that at all
1. [] Fix the graphics
1. [] Add traffic controls
1. [] Figure out the correct coordinates to upload the charging pads
1. [] Add weather conditions
1. [] Add NPC's
