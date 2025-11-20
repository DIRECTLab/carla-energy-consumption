# Demo Intructions

*How to run carlaUE4 for demos at showcases, events, etc.* 

## Ensure you have the carla server downloaded and setup on your machine. 

* You can clone the repository here: [carla repo](https://github.com/carla-simulator/carla/tree/ue4-dev?tab=readme-ov-file).
* Make sure to follow the CARLA teams [documentation](https://carla.readthedocs.io/en/0.9.14/build_linux/) for getting carla setup correctly.
* Other Helpful Docs for setup and configurations
    * [carla_install_help.md](./carla_install_help.md)
    * [create_world.md](./create_world.md)
    * [add_new_vehicle.md](./add_new_vehicle.md)
    * [steering_wheel_manual.md](./steering_wheel_manual.md)

## After setup is complete

### Current Method

1. Open a terminal
1. Navigate to the [PROJECTS_ROOT_FOLDER/](../)
1. Activate the `carlaclient-env` conda environment
    * If you cannot find the `carlaclient-env` env, navigate to [demo_helper_scripts/](../demo_helper_scripts/) and run `client.sh -i` this will install the conda env. Then retry from step 2. 
1. Run `python run_carla_demo.py`
    * See [run_carla_demo.py](../run_carla_demo.py)
    * It takes about 2 or 3 minutes then the demo will be ready to go.
    * Giving no options will run all the defaults for the demo.

Note:
* Options can be passed to [run_carla_demo.py](../run_carla_demo.py) just as if they are being passed to [client.sh](../demo_helper_scripts/client.sh).
  * Eg. `python run_carla_demo.py -a` will run the automated demo. 
* There is a help message you can see by running `python run_carla_demo.py -h` which will tell you how to use the options.

### More Manual Method

*This is more the older method for getting the demo running, still works but the current method is more automated.*

1. Starting the Carla Server
    1. Open a terminal
    1. Navigate to [demo_helper_scripts/](../demo_helper_scripts/) 
    1. Run `./server.sh`
        * See [server.sh](../demo_helper_scripts/server.sh)
        * If an error occurs about the pythonAPI/Boost see step 2 in [`carla_install_help.md`](./carla_install_help.md) for a solution.

1. Once the carla server is loaded, press play button in the Unreal Editor to
start the server.
    * Changing maps:
        * Best Demo Map: Town10HD (Don't do the Town10 HD OPT)
        * SLC Import Map: compiled_roads

1. Starting the CarlaCharge client
    1. Open a separate terminal
    1. Navigate to [demo_helper_scripts/](../demo_helper_scripts/)
    1. Run `./client.sh`
        * See [client.sh](../demo_helper_scripts/client.sh)
        * Note that the client will crash if you do not have a steering wheel connected to the machine when you run the script.
        * Run `run_carla_demo.sh -h` for help message on configuration options that are available.
