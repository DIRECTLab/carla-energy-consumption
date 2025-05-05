# Carla Setup with Unreal Engine 5
## Machine
* Working on `Ubuntu 22.04.5`
* Working in a conda env: `carlaUE5-env`

## Important links
* [Carla Site](https://carla.org/)
* [Carla Unreal Engine 5 docs](https://carla-ue5.readthedocs.io/en/latest/)
* [Carla Linux Build](https://carla-ue5.readthedocs.io/en/latest/build_linux_ue5/)
* [Extended Build Instructions](https://carla-ue5.readthedocs.io/en/latest/build_linux_ue5/#extended-build-instructions) These take the build step by step, instead of the all containing script, for more control should the main script have errors or greater configuration is needed.
* [Adding a New Vehicle](https://carla-ue5.readthedocs.io/en/latest/tuto_content_authoring_vehicles/)
* [PythonAPI docs for CarlaUE5](https://carla-ue5.readthedocs.io/en/latest/python_api/) There do seem to be some changes between the UE version used in Carla. May need to refactor our energy consumption extension to work again.
* [PythonAPI docs for CarlaUE4](https://carla.readthedocs.io/en/latest/python_api/)

## Disk Req
* Size of folders after install: TODO add

## Process, following non-extended build instructions
### Setup the environment
* Need to make a GitHub token, or setup SSH as the setup script needs this to clone the Unreal Engine repository, which must be linked to a GitHub account.
* Download of Carla Content took about 30 minutes.


## Errors and Fixes
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

* Attempted[x]: First I ran `conda install pip python=3.11` to get some main python pacakges and python itself in the environment.
* Attempted[x]: Ran `pip install build` from inside the conda env.
#### Fixed
* Added the following to the top of the `CarlaSetup.sh` script in the `CarlaUE5` directory.
    * `export PATH=/opt/cmake-3.28.3-linux-x86_64/bin:$PATH` This forced the script to recognize the cmake install as before, the build would fail saying the wrong version or missing cmake.
* Ran the setup script with all of the following modifiers. The python modifier to force use of the conda environment's python as before the build of the PythonAPI would fail as the script kept trying to use the base python interpreter which did not have the correct packages installed.
    * `sudo -E env GIT_LOCAL_CREDENTIALS=GITHUB_USERNAME@GITHUB_TOKEN ./CarlaSetup.sh --python-root=/home/carla/miniconda3/envs/carlaUE5-env/bin/`