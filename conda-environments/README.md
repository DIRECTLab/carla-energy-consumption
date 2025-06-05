# About the contents of this folder
### [client-carlaUE5.yml](./client-carlaUE5.yml)
* yml file to setup the conda client environment correctly. Note [run_carla.sh](../run_carla.sh) also will automatically make the carla client conda env for you if it does not exist.

### [server-carlaUE5.yml](./server-carlaUE5.yml)
* yml file to setup the conda server environment correctly.

### [Carla WHL file](./carla-0.10.0-cp311-cp311-linux_x86_64.whl)
* The Carla python package for Carla v0.10.0 is not on PIP as of writing this doc. This is the whl file to install the package. It was pulled from the files of the CarlaUE5 server.