# Carla Editor Setup with Unreal Engine 5
## Machine
* Working on `Ubuntu 22.04.5`
* Working in a Conda env: `server-carlaUE5`
* Working in a Conda env: `client-carlaUE5`

## Important links
* [Carla Site](https://carla.org/)

### Build Process
* [Carla Unreal Engine 5 docs](https://carla-ue5.readthedocs.io/en/latest/)
* [Carla Linux Build](https://carla-ue5.readthedocs.io/en/latest/build_linux_ue5/)
* [Extended Build Instructions](https://carla-ue5.readthedocs.io/en/latest/build_linux_ue5/#extended-build-instructions) These take the build step by step, instead of the all containing script, for more control should the main script have errors or greater configuration is needed.
* [Accessing Unreal Engine code on GitHub](https://www.unrealengine.com/en-US/ue-on-github)

### Useful
* [Adding a New Vehicle](https://carla-ue5.readthedocs.io/en/latest/tuto_content_authoring_vehicles/)
* [Carla Discord Discussions](https://github.com/carla-simulator/carla/discussions/)
* [Carla Discord Link](https://discord.com/invite/8kqACuC)

#### Speed Carla Up
* [Speed Up Carla FPS Post](https://github.com/carla-simulator/carla/discussions/8484) Comments that they sped up to 24/25 FPS by adding the -RenderOffScreen flag to the server.
* [Turn Off Screen Rendering Mode](https://carla-ue5.readthedocs.io/en/latest/adv_rendering_options/#off-screen-rendering-mode) It is looking like it might only be possible to do this with the CarlaUE5 quick build, not the build with the Unreal Editor.

## General Disk Requirements
* `UnrealEngine5_carla` ->, 163Gb
* `CarlaUE5` -> 76Gb
* `client-carlaUE5` Conda environment -> 1.4Gb
* `server-carlaUE5` Conda environment -> 328 Mb
* `carla-energy-consumption` -> 138Mb



## Process, following non-extended build instructions
### Setup the environment - Building the PythonAPI
* Need to make a GitHub token, or setup SSH as the setup script needs this to clone the Unreal Engine repository, which must be linked to a GitHub account.
* Download of Carla Content took about 30 minutes.
* Command that worked to fully setup the Unreal Editor, run it in the root of the `CarlaUE5` directory.
  * `sudo -E env GIT_LOCAL_CREDENTIALS=GITHUB_USERNAME@GITHUB_TOKEN ./CarlaSetup.sh --python-root=/home/carla/miniconda3/envs/server-carlaUE5/bin/`
  * Make a classic github token with your account. Note, your github account needs to be linked to EpicGames to the Unreal Repo.
* Have to run these so Unreal can start without using sudo
  1. `sudo chown -R $USER:$USER /home/carla/CarlaUE5/Build/`
  2. `sudo chown -R $USER:$USER /home/carla/CarlaUE5/PythonAPI/`
  3. `sudo chown -R $USER:$USER /home/carla/CarlaUE5/Unreal/`
    * As one command: `sudo chown -R $USER:$USER /home/carla/CarlaUE5/Build/ && sudo chown -R $USER:$USER /home/carla/CarlaUE5/PythonAPI/ && sudo chown -R $USER:$USER /home/carla/CarlaUE5/Unreal/`

### Launching the Editor After Build/Source changes
* Run `sudo -E /opt/cmake-3.28.3-linux-x86_64/bin/cmake --build Build --target launch` first. 
  * Probably need to go back and build things so running works better, however this way does work for now. Have to run to actually build as somethings are locked as root permission during the build process.
* Run `cmake --build Build -t launch` (-t or --target) in the root directory of `CarlaUE5` in the `server-carlaUE5` Conda env.
  * Have to run again without `sudo` as UnrealEngine will refuse to start with root permissions.
* Note: Once the Setup is done, only need to run this command to relaunch the Carla UE Editor/Server

## Launching the Editor Otherwise
* Run `cmake --build Build -t launch` (-t or --target) in the root directory of `CarlaUE5` in the `server-carlaUE5` Conda env.

### Working Editor
* Click the play button to make ready for client to connect.
* Run `./run_carla.sh` in the root directory of `carla-energy-consumption`
* PyGame window should come up with the Lincoln example car. Able to drive with the steering wheel.
  * Note: Will crash if the steering wheel is not connected before starting client.


## Errors and Fixes
* Note: When a command is run with `sudo` permission. All of the environment variables are reset for security. So if you need the environment variables for the command to work, you have to add the `-E` modifier to preserve the environment. This has caused a lot of errors.

### Error at setup
* I got this error running the script which basically does everything to download, build and start.
* `sudo -E env GIT_LOCAL_CREDENTIALS=github_username@github_token ./CarlaSetup.sh`
* Ran the command, according to docks this does pretty much all of the setup. Got the following error in the command line.
```bash                                                                                  
Err:16 https://apt.llvm.org/jammy llvm-toolchain-jammy-10 Release                                                                                                               
    404  Not Found [IP: 199.232.66.49 443]
```
(other working stuff)
```bash     
E: The repository 'http://apt.llvm.org/jammy llvm-toolchain-jammy-10 Release' does not have a Release file.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
```

#### Fixed
* Commented it out from the update list, I am not sure if Carla actually needs the repository that is causing issues. As chatGPT saying the jammy-10 does not exist for Ubuntu 22.04. This did allow the setup to continue.
---


### Permission denied for access to Unreal repo
* Got all of the Carla Contents through, but now keeps having permission issues when trying to install the UnrealEngine. I have linked my account and I shared an access token, not sure why it is not seeing the permission. 
```bash
Cloning into 'UnrealEngine5_carla'...
remote: Write access to repository not granted.
fatal: unable to access 'https://github.com/CarlaUnreal/UnrealEngine.git/': The requested URL returned error: 403
```
* The script will detect if the Carla Contents were already downloaded. You can rerun the setup script without having to redownload alll of the Carla Contents.
* I think I setup my GitHub access token wrong.

#### Fixed
* Had to make a new GitHub "classic" token with `repo` permissions, my credentials for accessing the Unreal repo were then recognized.
---


### Failed at the End of Build
* Failed near what I think was the end of the super script `./CarlaSetup.sh --interactive`. I believe it failed when trying to build the PythonAPI.
* I think this might be because of my Conda environment. I think the super script pip installs packages. Though those should still be visible to the environment? Not sure.
* Looking more into my Conda environment, it looks like the main setup script failed to actually install any of the packages in Conda. I think to fix this I will have to go through the step by step setup instead and make sure the packages install to Conda.
* Though, I do believe the Unreal Engine compiled successfully, so I should be able to skip to the PythonAPI setup/only do steps that involve python packages. Took almost 2 hours to build the Unreal Engine.

```bash
[444/444] Linking CXX static library LibCarla/libcarla-server.a
Installing Python API...
[0/2] Re-checking globbed directories...
[0/2] cd /home/carla/CarlaUE5/PythonAPI/c...rla/CarlaUE5/Build/PythonAPI/dist --wheel
/usr/bin/python3.11: No module named build
FAILED: PythonAPI/CMakeFiles/carla-python-api /home/carla/CarlaUE5/Build/PythonAPI/CMakeFiles/carla-python-api 
cd /home/carla/CarlaUE5/PythonAPI/carla && /opt/cmake-3.28.3-linux-x86_64/bin/cmake -E copy /home/carla/CarlaUE5/LICENSE /home/carla/CarlaUE5/PythonAPI/carla/LICENSE && /usr/bin/python3.11 -m build --outdir /home/carla/CarlaUE5/Build/PythonAPI/dist --wheel
ninja: build stopped: subcommand failed.
```

```bash
(carlaUE5-env) carla@gaston-System-Product-Name:~/CarlaUE5$ cmake --preset Development
Preset CMake variables:

  CMAKE_BUILD_TYPE="RelWithDebInfo"
  CMAKE_EXPORT_COMPILE_COMMANDS:BOOL="TRUE"
  CMAKE_INSTALL_PREFIX:PATH="/home/carla/CarlaUE5/Install/Development"
  CMAKE_TOOLCHAIN_FILE="/home/carla/CarlaUE5/CMake/Toolchain.cmake"

CMake Error at CMake/Toolchain.cmake:25 (message):
  The specified Carla Unreal Engine 5 path does not exist ("").
Call Stack (most recent call first):
  /opt/cmake-3.28.3-linux-x86_64/share/cmake-3.28/Modules/CMakeDetermineSystem.cmake:170 (include)
  CMakeLists.txt:40 (project)


CMake Error: CMake was unable to find a build program corresponding to "Ninja".  CMAKE_MAKE_PROGRAM is not set.  You probably need to select a different build tool.
CMake Error: CMAKE_C_COMPILER not set, after EnableLanguage
CMake Error: CMAKE_CXX_COMPILER not set, after EnableLanguage
CMake Error: CMAKE_ASM_COMPILER not set, after EnableLanguage
-- Configuring incomplete, errors occurred!

```

#### Attempted Fixes
* First I ran `conda install pip python=3.11` to get some main python pacakges and python itself in the environment.
* Ran `pip install build` from inside the Conda env.

#### Fixed
* Added the following to the top of the `CarlaSetup.sh` script in the `CarlaUE5` directory.
    * `export PATH=/opt/cmake-3.28.3-linux-x86_64/bin:$PATH` This forced the script to recognize the cmake install, as before the build would fail saying the wrong version or missing cmake.
    * Reinstalled cmake, putting it into `/opt`. 
* Ran the setup script with all of the following modifiers. The python modifier forces use of the Conda environment's python interpreter as before the build of the PythonAPI would fail as the script kept trying to use the base env python interpreter which does not have the correct packages installed.
    * `sudo -E env GIT_LOCAL_CREDENTIALS=GITHUB_USERNAME@GITHUB_TOKEN ./CarlaSetup.sh --python-root=/home/carla/miniconda3/envs/server-carlaUE5/bin/`
---


### Failed at the very end to Launch
Command: `sudo -E /opt/cmake-3.28.3-linux-x86_64/bin/cmake --build Build --target launch`  
Output:
```bash
[24/27] Link (lld) libUnrealEditor-Carla.so (UBA disabled)
[25/27] Link (lld) libUnrealEditor-CarlaUnreal.so (UBA disabled)
[26/27] Link (lld) libUnrealEditor-CarlaTools.so (UBA disabled)
[27/27] WriteMetadata CarlaUnrealEditor.target (UBA disabled)
Trace file written to /home/carla/UnrealEngine5_carla/Engine/Programs/UnrealBuildTool/Log.uba with size 11.9kb
Total time in Unreal Build Accelerator local executor: 119.43 seconds
Total execution time: 124.88 seconds
[15/16] Launching Carla Unreal...
Refusing to run with the root privileges.
libc++abi: __cxa_guard_acquire detected recursive initialization
Aborted (core dumped)
FAILED: Unreal/CMakeFiles/launch /home/carla/CarlaUE5/Build/Unreal/CMakeFiles/launch 
cd /home/carla/CarlaUE5/Build/Unreal && /home/carla/UnrealEngine5_carla/Engine/Binaries/Linux/UnrealEditor /home/carla/CarlaUE5/Unreal/CarlaUnreal/CarlaUnreal.uproject -vulkan -log --ros2
ninja: build stopped: subcommand failed.
```
* This issue seems to be because Unreal refuses to run with Sudo permissions, however when I do not run the command with Sudo permission, then I get this.
Output
```bash
[0/2] Re-checking globbed directories...
ninja: error: rebuilding 'build.ninja': Error writing to build log: Permission denied
```
* Which is implying `ninja` cannot be accessed without sudo rights.
* Used `sudo` alot during building to get things working, which now is turning out to be a problem. As Unreal won't run as `sudo` and setting up things with `sudo` locked permissions from the user `carla`.

#### Fixed
Changing those permissions worked! The Carla Unreal 5 Editor is now working!
1. `sudo chown -R $USER:$USER /home/carla/CarlaUE5/Build/`
2. `sudo chown -R $USER:$USER /home/carla/CarlaUE5/PythonAPI/`
3. `sudo chown -R $USER:$USER /home/carla/CarlaUE5/Unreal/`
(TODO I could add these as part of the build script, or rework the setup to not use `sudo` in spots that make it not work at the end somehow.)
---


### Error getting client to connect to server
Command: `./run_carla.sh` ran in the client env in `carla-energy-consumption`
Output
```bash
(base) carla@gaston-System-Product-Name:~/carla-energy-consumption$ ./run_carla.sh 
Carla conda env exists, skipping installation...
Traceback (most recent call last):
  File "navigation/draw_chargers.py", line 54, in <module>
    world = client.get_world()
RuntimeError: time-out of 20000ms while waiting for the simulator, make sure the simulator is ready and connected to 127.0.0.1:2000
```
* Client not recognizing that the server is running.
* Output from `netstat -an` while the carla server running. From two different times, I restarted the server and these same ports came up as listening. I am not sure which one is the carla server. I suppose I am not sure that the carla server is even listening, but I think it is. Which in that case either need to find where you can set the default port Carla Server uses, or change the default port the client will use.
```bash
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:5345          0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:8558          0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN     
......
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:5345          0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:8558          0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN     
```
* According to the documentation the carlaUE5 still listens on port 2000 by default, so either that default got changed somehow or the server is not actually listening for anything.

#### Attempted Fixes
* Just realized `client-carlaUE5` env has the wrong version of the carla python package installed. It has `0.9.15`, my server has `0.10.0`
  * Going to update this and see if it gets things working.

#### Fixed
* I realized I was not clicking the play button on the server side, which is necessary for the client to actually connect.
* The `client-carlaUE5` had the wrong version of carla. Got that updated to `carla 0.10.0`.
  * Got carla 0.10.0 installed with `pip install /home/carla/CarlaUE5/Build/PythonAPI/dist/carla-0.10.0-cp311-cp311-linux_x86_64.whl`
  * Using the local wheel file in `~/CarlaUE5/Build/PythonAPI/dist` as `carla 0.10.0` does not show up on `pip`.
* I did some other version matching, I unfortunately did not test it before trying some other things. However, I believe that the connection problem was fixed once the carla version was correct, though may have come from the other version match fixes. As the drawn charger squares show up on the server now when you run `run_carla.sh` client side. It is connecting now.
---


### Pygame screen flashes but does not stay
* Now the client seems to connect but pygame screen not staying/working.
* I say it is connecting because when the client is run, the charger pad squares are drawn in the server. They look a different from the Unreal4, though. They are darker colored, and
 a little stuck in the ground.
* Output:
  ```bash
  (client-carlaUE5) carla@gaston-System-Product-Name:~/carla-energy-consumption$ ./run_carla.sh 
  Carla client conda env exists, skipping installation...
  Waiting for Ctrl-C
  ```
* Looking around the map more, it does look like the charger boxes are being drawn onto the map which is cool.
* I cloned the old `carlaenv` to make the new `client-carlaUE5` but when updating the python version it must have deleted packages that were needed like `pygame`, `panda`, others. Not sure why, still learning how Conda works exactly. But I think it shoudl fix things once I get those packages added back correctly
* I think I messed up the Conda client env by cloning it from the old one then trying to switch the python version. Ended up installing a bunch of sub libraries and trying to patch dependency issues, which eventually caused strange dependency locks where I could not install needed packages.

#### Attempted Fixes
* Deleted the client env twice, it. Better idea, going to make a new one, with the newer version of python and carla. Then just install the packages `run_carla.sh` calls for. Better than all the random stuff I installed just looking at the Conda list from `carlaenv`. 
  * I am going try to rebuild now, setting the python interpreter of `server-carlaUE5` env to be `Python 3.11.8` so it matches the client (client had to be `Python 3.11.8` for other dependencies it needed, according to Conda.)
  * The PyGame screen does come up now, so getting close but just flashes then disappears. Not sure what the problem is.

* I realized the `run_carla.sh` script was suppressing all terminal output, so I made a debug version that does not suppress output to see the errors.
* Output:
  ```bash
  (client-carlaUE5) carla@gaston-System-Product-Name:~/carla-energy-consumption$ ./run_carla.sh 
  Carla client conda env exists, skipping installation...
  <frozen importlib._bootstrap>:241: RuntimeWarning: Your system is avx2 capable but pygame was not built with support for it. The performance of some of your blits could be adversely affected. Consider enabling compile time detection with environment variables like PYGAME_DETECT_AVX2=1 if you are compiling without cross compilation.
  pygame 2.6.1 (SDL 2.32.50, Python 3.11.8)
  Hello from the pygame community. https://www.pygame.org/contribute.html
  Waiting for Ctrl-C
  vehicle Name
  vehicle
  INFO: listening to server 127.0.0.1:2000

  Welcome to CARLA manual control with steering wheel Logitech G29.

  To drive start by pressing the brake pedal.
  Change your wheel_config.ini according to your steering wheel.

  To find out the values of your steering wheel use jstest-gtk in Ubuntu.


  Traceback (most recent call last):
    File "/home/carla/carla-energy-consumption/manual_control_steeringwheel.py", line 170, in <module>
      main()
    File "/home/carla/carla-energy-consumption/manual_control_steeringwheel.py", line 162, in main
      Simulation(args)
    File "/home/carla/carla-energy-consumption/manual_control_steeringwheel.py", line 55, in __init__
      self.__world = World(
                    ^^^^^^
    File "/home/carla/carla-energy-consumption/interface/world.py", line 48, in __init__
      self.restart()
    File "/home/carla/carla-energy-consumption/interface/world.py", line 56, in restart
      blueprint = random.choice(self.world.get_blueprint_library().filter(self._actor_filter))
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/carla/miniconda3/envs/client-carlaUE5/lib/python3.11/random.py", line 373, in choice
      raise IndexError('Cannot choose from an empty sequence')
  IndexError: Cannot choose from an empty sequence
  double free or corruption (out)
  ```

#### Fixed
* The example vehicle csv was the issue. Orignally this was in `tesla.csv`, `vehicle.tesla.model3`. This accessor did not work with the PythonAPI, the built in Tesla must have different accessor names. It was taking too long to find the correct accessors for the Tesla.
* Switched example to be `lincoln.csv`, with the working accessor `vehicle.lincoln.mkz`.
* With that switch, the Pygame console now loads, and User is able to drive the vehicle with the steering wheel! The charging part also functions, when driving the vehicle on top of one of the pads, the increase in charge power is recognized in the HUD stats.
---


### Charging pad outlines are appearing partially in the ground
* Must be some issue with the z-axis that is being calculated for the csv file.
* `charger_options.py` is supposedly the file that handles generation for the csv files that place the chargers in the map. However it is missing.

#### Recreating the Town10_intersection_chargers.csv based on the new map 10

* 
* front_left = "(41.04231262207031,53.58794403076172,1.7484555314695172e-07)"
* front_right = "(40.042396545410156,53.601051330566406,1.7484555314695172e-07)"
* back_right = "(40.01618194580078,51.601226806640625,-1.7484555314695172e-07)"
* power = 100000.0
* efficiency = 0.95

* front_left = "(57.981632232666016,66.82268524169922,0.0)"
* front_right = "(57.982913970947266,65.82268524169922,0.0)"
* back_right = "(59.982913970947266,65.82524871826172,0.0)"
* power = 100000.0
* efficiency = 0.95

* map=`Town10HD_Opt`
* power = 100000.0
* efficiency = 0.95
* length = 2
* width = 1

* Well, I was able to correctly generate a chargers csv for the town 10 map with this command. THat is progess. 
  * `python junction_chargers_all.py --power 100000.0 --efficiency 0.95 -m Town10HD_Opt 2 1 testing-chager-creation`
  * I did delete the files I created as I did not want to save them. Can add create again later.
* But even though it regenerated based off of the UE5 version of map 10 the charger boxes are still in the ground weirdly.
  * Will need to look at the actual calculations for the Z-coordinate of teh chargers.
* I messed with some of the values, maybe I can mess with the values of one and see how to get it right. Also need to check out how the z-coordinate is generated.

---


## TODOs ls -l /home/carla/CarlaUE5
1. Shut off background display to speed things up
2. fix the charging pads, z-axis
3. Figure out the Reinforcement learning plugin for Unreal Engine 5


## Current Status
* Carla Editor and Carla client for manual driving are both working with the UE5 on map 10!

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