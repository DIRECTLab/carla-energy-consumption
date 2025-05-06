# Carla Setup with Unreal Engine 5
## Machine
* Working on `Ubuntu 22.04.5`
* Working in a conda env: `server-carlaUE5`
* Working in a conda env: `client-carlaUE5`

## Important links
* [Carla Site](https://carla.org/)
* [Carla Unreal Engine 5 docs](https://carla-ue5.readthedocs.io/en/latest/)
* [Carla Linux Build](https://carla-ue5.readthedocs.io/en/latest/build_linux_ue5/)
* [Extended Build Instructions](https://carla-ue5.readthedocs.io/en/latest/build_linux_ue5/#extended-build-instructions) These take the build step by step, instead of the all containing script, for more control should the main script have errors or greater configuration is needed.
* [Adding a New Vehicle](https://carla-ue5.readthedocs.io/en/latest/tuto_content_authoring_vehicles/)
* [PythonAPI docs for CarlaUE5](https://carla-ue5.readthedocs.io/en/latest/python_api/) There do seem to be some changes between the UE version used in Carla. May need to refactor our energy consumption extension to work again.
* [PythonAPI docs for CarlaUE4](https://carla.readthedocs.io/en/latest/python_api/)

* [Carla Forum](https://github.com/carla-simulator/carla/discussions/)
* [Carla Discord Link](https://discord.com/invite/8kqACuC)

## Disk Req
* Size of folders after install: TODO add

## Process, following non-extended build instructions
### Setup the environment
* Need to make a GitHub token, or setup SSH as the setup script needs this to clone the Unreal Engine repository, which must be linked to a GitHub account.
* Download of Carla Content took about 30 minutes.

* Had to run the launch command in the following way to work properly. It kept having the error where it would not find cmake.
* Put the absolute path to cmake in the command.
`sudo -E /opt/cmake-3.28.3-linux-x86_64/bin/cmake --build Build --target launch`

### Launch the Editor
`cmake --build Build --target launch` in server env


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
* Attempted[x]: Going to comment it out from the update list, I am not sure if Carla actually needs the repository that is causing issues. As chatGPT saying the jammy-10 does not exist for Ubuntu 22.04
* Result: This did allow the setup to continue. Should not cause an issue later.
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
* Attempted[x]: Had to make a new GitHub "classic" token with `repo` permissions, this worked. 
* Result: My credentials for accessing the Unreal repo were recognized.
---

### Failed at the End of Build
* Failed near what I think was the end of the super script `./CarlaSetup.sh --interactive`. I believe it failed when trying to build the PythonAPI.
* I think this might be because of my conda environment. I think the super script pip installs packages. Though those should still be visible to the environment? Not sure.
* Looking more into my conda environment, it looks like the main setup script failed to actually install any of the packages in conda. I think to fix this I will have to go through the step by step setup instead and make sure the packages install to conda.
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
* Ran `pip install build` from inside the conda env.

#### Fixed
* Added the following to the top of the `CarlaSetup.sh` script in the `CarlaUE5` directory.
    * `export PATH=/opt/cmake-3.28.3-linux-x86_64/bin:$PATH` This forced the script to recognize the cmake install, as before the build would fail saying the wrong version or missing cmake.
* Ran the setup script with all of the following modifiers. The python modifier to force use of the conda environment's python as before the build of the PythonAPI would fail as the script kept trying to use the base python interpreter which did not have the correct packages installed.
    * `sudo -E env GIT_LOCAL_CREDENTIALS=GITHUB_USERNAME@GITHUB_TOKEN ./CarlaSetup.sh --python-root=/home/carla/miniconda3/envs/carlaUE5-env/bin/`
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
* Used `sudo` alot during building to get things working, which now is turning out to be a problem. As Unreal won't ran as `sudo` and setting up things with `sudo` locked permissions from the user `carla`.
* Getting lots more permission issues. Been running this command on a couple of folders in `CarlaUE5` to move permissions back to the user. Doing so has been making the launch go longer not being run as sudo, has not failed yet.

#### Fixed
TODO I could add these as part of the build script, I think
1. `sudo chown -R $USER:$USER /home/carla/CarlaUE5/Build/`
2. `sudo chown -R $USER:$USER /home/carla/CarlaUE5/PythonAPI/`
3. `sudo chown -R $USER:$USER /home/carla/CarlaUE5/Unreal/`
* Changing those permissions worked! The Carla Unreal 5 Editor is now working!

### Error getting client to connect to server
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

#### Attempted Fixes TODO
* Change up accessors for the test vehicles in the client's csv's
* One thoguht is that the carla-environment package maybe needs to be updated to work with carlaUE5. So going to make a new conda env which could be updated hopefully.


* `conda remove --name carlaUE5-env --all` renamed this conda env to be `server-carlaUE5`, I thought better naming.
* This broke stuff. Note to self there is more to a conda env than just running the copy command.
* Fixed it, had to rerun the setup with the new path to the python interpreter in my renamed conda env
  * `sudo -E env GIT_LOCAL_CREDENTIALS=GITHUB_USER@GITHUB_TOKEN ./CarlaSetup.sh --python-root=/home/carla/miniconda3/envs/server-carlaUE5/bin/`
  * TODO: write result. I am going try to rebuild now, setting the python version to be 3.11.8 so it matches the client (client has to be 3.11.8 for other dependencies it needed.)
* Just realized conda client env has the wrong version of the carla python package installed. It has `0.0.15`, my server has `0.10.0`
  * Going to update this and see if it gets things working.

* Got carla 0.10.0 installed with `pip install /home/carla/CarlaUE5/Build/PythonAPI/dist/carla-0.10.0-cp311-cp311-linux_x86_64.whl`
  * Using the local wheel, as carla 0.10.0 does not show up on pip
  * Also upgraded to python 3.11.8 to match the server env, which might fix this issue?

### Getting close but no pygame/control screen
* I realized I was not clicking the play button on the server side, which is necessary for the client to actually connect.
* Now the client seems to connect but nothing happens?
* Output:
  ```bash
  (client-carlaUE5) carla@gaston-System-Product-Name:~/carla-energy-consumption$ ./run_carla.sh 
  Carla client conda env exists, skipping installation...
  Waiting for Ctrl-C
  ```
* Which looking around the map more, it does look like the charger boxes are being drawn onto the map which is cool. However the pygame screen is no longer coming up like before. Which I am thinking could have something to do with my versions in the conda env. Going to try to update pygame in there.
* Yes that is the issue. I cloned the old `carlaenv` to make the new `client-carlaUE5` but when updating the python version it must have deleted packages that were needed like `pygame`, `panda`, others. Not sure why, still learning how conda works exactly. But I think it shoudl fix things once I get those packages added back correctly

* deleted the client env twice. Better idea, going to make a new one, with the newer version of python and carla. Then just install the things `run_carla.sh` call for. Better than all the random stuff I installed just looking at the conda list from `carlaenv`. I think I ended up installing a bunch of sub libraries which maybe messed things up? Cause after installiing all that, the pygame window would come up but only for a second then dissapear.
  * It forced to change to python 3.11.8, maybe I will need to rebuild Carla Server with that instead of 3.11.11. Does it matter?