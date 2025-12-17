# Todos for the Carla Project 

## In Progress

## Priority

1. [] Create a yml file so the client conda env is easily reproducible on another machine
1. [] Create a yml file so the server conda env is easily reproducible on another machine

## Backlog

1. [] Write up in the docs or notes how the desktop shortcut works so next guy can figure it out should there be issues.
1. [] Is there a more robust way than explicitly putting the path to UE4 in the server script to get the desktop shortcut start way working? Thinking about setting this up on other machines than just the one carla machine.
1. [] Clean up the demo files themselves now that things are working to be more optimized
1. [] Update [add_new_vehicle.md](./add_new_vehicle.md) to match the new ways of running carla 
1. [] Create a setup script that automates the setup process for the Carla server.
    * Install all dependencies into a new Conda env
1. [] Fully thresh out the unreal 5 branch to upgrade to Carla Unreal 5
1. [] Fix up that SLC map we created
    * Fix the graphics
    * Add traffic controls
    * Add weather conditions
1. [] Figure out the best way to not have roads just dying or if I need to change that at all

## Completed

1. [x] Add to World creator docs which version using and how Zac did it.
1. [x] Get Carla demo able to run from desktop icon
1. [x] Make sure docs are updated to reflect the new way to run carla
1. [x] Clean up the scripts so all paths work and the layout is more intuitive with the addition of the new script/way to run carla
1. [x] move the `notes` directory into the docs folder, and cleanup links as needed
1. [x] rename the various demo files to have a more intuitive naming system
1. [x] refactor the `run_carla_demo.sh` script to make demos even easier
    * [x] Start with kenworth as default
    * [x] to be able to run the manual and/or the automated demo
1. [x] Fix the HUD
    * Speed
    * SOC percentage
    * Energy Consumption
    * Regenerative Braking
1. [x] Get Aaron's work modularized
1. [x] write docs for how to move a created map from one machine to another.
