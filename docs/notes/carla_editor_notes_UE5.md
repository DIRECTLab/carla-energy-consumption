## Current Status
* Carla Editor and Carla client for manual driving are both working with the UE5 on map 10!
* Able to import kenworth truck and drive it around, it also does recognize the charging pads when driven over them.

## TODOs
1. Shut off background display to speed things up
2. fix the charging pads, z-axis
3. Figure out the Reinforcement learning plugin for Unreal Engine 5
4. Speed up Carla!


## Longterm Goals
* Integrate reinforcement learning into Carla (through the PythonAPI)
  * Able to command the vehicle and it drives properly going from one place to the other.
  * Get the charging data as it's going for learning.


## Reinforcement Learning with Carla
### TODO Links to read
* [End-to-end learning using CARLA Simulator](https://imtiazulhassan.medium.com/end-to-end-learning-using-carla-simulator-12869b5d6f7)
    * Will I need to get the ROS bridge working to do reinforcement learning? I know they supposedly made it more integrated or easier or something in carlaUE5 to use the ROS.


## Speed Carla Up
* [Speed Up Carla FPS Post](https://github.com/carla-simulator/carla/discussions/8484) Comments that they sped up to 24/25 FPS by adding the -RenderOffScreen flag to the server.
* [Turn Off Screen Rendering Mode](https://carla-ue5.readthedocs.io/en/latest/adv_rendering_options/#off-screen-rendering-mode) It is looking like it might only be possible to do this with the CarlaUE5 quick build, not the build with the Unreal Editor.

### FPS
All felt pretty smooth except for the full screen res, which was still pretty good but felt slightly slow here and there
* Full screen resolution on this machine. (3440x1440)
  * client running at about 60
  * server at 9-10
* 1920x1080
  * client about 60
  * server 14-15
* 1366x768
  * Around 60
  * 17-18
* 1440x900
  * Around 60
  * 16-17

## Useful
* Note: When a command is run with `sudo` permission. All of the environment variables are reset for security. So if you need the environment variables for the command to work, you have to add the `-E` modifier to preserve the environment.