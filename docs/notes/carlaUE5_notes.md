# My notes for getting CarlaUE5 editor working and integrating RL with the charger pads.
## Current Status
* Carla Editor and Carla client for manual driving are both working with the UE5 on map 10!
* Able to import kenworth truck and drive it around, it also does recognize the charging pads when driven over them.
* The Kenworth truck will drive automatically, albeit not very well (cuts corners and can make bad turns where it hits a boundary and gets stuck not knowing to back up) 

## Kenworth Truck Notes
* I made my own Torque Curve, will need to get data or something on a true EV 6 wheeler truck torque curve.
  * Gears settings default.
* Changed the set mass to 9752Kg, hoping that will make it drive more like an actual semi.
  * Was set at 1800Kg before.
  * Upon changing, the truck does not move anymore, I think I need to change up the torque curve.
  * Changed the Max Torque to 5000. The truck does move now, however it drives with some odd behavior.
    * Weird bouncing at times where the road appears to be smooth.
    * It seems to keep hitting bumps in the road that are not there.
    * Struggles to make turns nicely (swings too wide, hitting other vehicles and obstacles)

## TODOs
1. fix the charging pads, z-axis
1. Figure out the Reinforcement learning plugin for Unreal Engine 5
1. Speed up Carla!
1. Fix the kenworth truck so it is driving well
1. Add a working trailer to the kenworth
  * How do we work with more than four wheels that move?

## Longterm Goals
* Integrate reinforcement learning into Carla (through the PythonAPI)
  * Able to command the vehicle and it drives properly going from one place to the other.
  * Get the charging data as it's going for learning.


## Speed Carla Up
* [Speed Up Carla FPS Post](https://github.com/carla-simulator/carla/discussions/8484) Comments that they sped up to 24/25 FPS by adding the -RenderOffScreen flag to the server.
* [Turn Off Screen Rendering Mode](https://carla-ue5.readthedocs.io/en/latest/adv_rendering_options/#off-screen-rendering-mode) It is looking like it might only be possible to do this with the CarlaUE5 quick build, not the build with the Unreal Editor.

### FPS
All felt pretty smooth except for the 3440x1440 res, which is somewhat jumpy
* 3440x1440
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



# My Old Notes from laptop
*Was called `carla-charge-task`*
## my work
* understand the sim
* make the paper better
* run the sim
* develop new scenarios that are from the SLC where the electric roadways will go
    * semi charging pad
* Fix the Semi Truck (only handling 4 wheels, semi has 6)
* New roadway scenes
* AirGap problems
* Costing analysis
* add some more scenarios
* rewrite part of the paper

# Notes Getting Carla Running again on Waluigi
* Thus far have tried running through a lot fo the Software requirements steps to see if things were missing.
* Just recompiled the UnrealEngine.
    * While I was going through Software Requirements steps again, an error came up that a file had been modified in the Unreal files, I had it overwrite it.
    * That did seem to fix something, before when I tried to open the Unreal editor it would fail.
    * Success, I can get the unreal editor open.
* Still having the same error. Saying stdin not in gzip format. Some issue when running `make PythonAPI`, the issue is with it trying to get the package: Boost.
    * Some ChatGPT help. Pointed out the file it is downloading is way too small to actually be Boost. So the issue seems to be with the location it is trying to pull from when making the PythhonAPI
* I recloned the Carla repository. Now I am rerunning the steps on setting that up, we will see if that fixes the issue.

# Notes Getting Carla Running
* I started doing a script recording, so I can go back and see what the console said if there are issues later. I will do one for each day I think that will be a good idea. Should be helpful to remember what exactly I did.

* Pretty much followed these intstructions to the letter and things worked, [LinuxCarlaSetup](http://carla.readthedocs.io/en/latest/build_linux/)

TODO end the script record for the day

## Software Requirements
* When I ran this command `wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key|sudo apt-key add` the output said it was successful but that the apt-key was depricated. Is this important?
### Unreal Engine
* You do have to link the github account that you use to clone down Carla to an EpicGames/Unreal Engine account.
* Making the build takes a while. Started on my machine at 14:35, finished building at 15:58

## part 2 Build Carla 
* Run all the commands here in the `carla` directory

### Build Carla
* Downloaded aria2

#### compile client
* Compile Python API on first build of Carla and after any updates.
* `make PythonAPI`
    * Error occured here first time I ran. I believe this is beacause I did not have the clang compiler in my environment variable so it could not find it. Adding to environment variable seems to have fixed it, build was successful.
* Us `.egg` file or `.whl`. `.egg` is supposedly older but should come preinstalled, I am going to try it with that first, if it does not work I will come back to this step and will install the whl

#### compile server
* Started `make launch` (compiling server) at 09:25, failed at 09:42
    * During compilation gave me this message "update code to the new API before update or will not work" (paraphrase)
        * How to get this updated API?
    * It failed after I unplugged my extra monitors, which I thought would speed things up. (It seemed to help speed things up/get it unstuck yesterday when I was compiling the Unreal engine). Going to try again and not mess with it when it starts to freeze up the mouse, I will just leave it.
    * The error message
        ```
        [2025.04.29-15.39.10:652][  0]LogShaderCompilers: Display: Worker (3/13): shaders left to compile 4910
        [2025.04.29-15.39.10:652][  0]LogStaticMesh: Building static mesh SM_SkyscraperNY_02_v03_merged...
        [2025.04.29-15.39.12:736][  0]LogShaderCompilers: Display: Worker (1/13): shaders left to compile 4900
        [2025.04.29-15.39.38:157][  0]LogAudioMixer: Display: Audio Buffer Underrun (starvation) detected.
        [2025.04.29-15.39.38:163][  0]LogAudioMixer: Display: Audio Buffer Underrun (starvation) detected.
        [2025.04.29-15.39.38:163][  0]LogAudioMixer: Display: Audio Buffer Underrun (starvation) detected.
        /home/tysonb/carla-charge-stuff/carla/Util/BuildTools/BuildCarlaUE4.sh: line 209: 59939 Killed                  ${GDB} ${UE4_ROOT}/Engine/Binaries/Linux/UE4Editor "${PWD}/CarlaUE4.uproject" ${RHI} ${EDITOR_FLAGS}
        make: *** [Util/BuildTools/Linux.mk:8: launch] Error 137

        ```

    * Restarted `make launch` at 09:49, failed again with the same error at 9:59

