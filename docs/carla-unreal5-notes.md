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

### Attempting Extended Build Instructions (does the building one step at time)
* [Extended Build Instructions](https://carla-ue5.readthedocs.io/en/latest/build_linux_ue5/#extended-build-instructions)
* The error is just from `sudo apt update`, just got the same error from running that alone.
```bash
(carlaUE5-env) carla@gaston-System-Product-Name:~/CarlaUE5$ grep -r "llvm-toolchain-jammy-10" /etc/apt/sources.list.d/
/etc/apt/sources.list.d/archive_uri-http_apt_llvm_org_jammy_-jammy.list:deb http://apt.llvm.org/jammy/ llvm-toolchain-jammy-10 main
/etc/apt/sources.list.d/archive_uri-http_apt_llvm_org_jammy_-jammy.list:# deb-src http://apt.llvm.org/jammy/ llvm-toolchain-jammy-10 main
```
The file where I commented out, which is odd it looked like there was already the same item in that file which was commented out already.

* Result: Commenting that out did fix the errror, will need to test if that was needed for the Carla Sim
