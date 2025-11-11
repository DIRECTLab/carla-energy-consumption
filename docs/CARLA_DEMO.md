# Demo Intructions
*How to run carlaUE4 for demos at showcases, events, etc.* 

1. Ensure you have the carla server downloaded and setup on your machine. 
    * You can clone the repository here: [carla repo](https://github.com/carla-simulator/carla/tree/ue4-dev?tab=readme-ov-file).
    * Make sure to follow their [documentation](https://carla.readthedocs.io/en/latest/) for getting carla setup correctly.
    * Other Helpful Docs for setup and configurations
        * [`carla_install_help.md`](./carla_install_help.md)
        * [`create_world.md`](./create_world.md)
        * [`add_new_vehicle.md`](./add_new_vehicle.md)
        * [`steering_wheel_manual.md`](./steering_wheel_manual.md)

1. Starting the Carla Server
    1. Open a terminal
    1. Activate the server conda env: `carlaenv`
        * Run `conda env list` to see all available conda envs
    1. Move into the `carla` directory
    1. Run `make launch`
        * If an error occurs about the pythonAPI/Boost follow step 2 in 
        [`carla_install_help.md`](./carla_install_help.md) for a solution.

1. Once the carla server is loaded, press play button in the Unreal Editor to
start the server.
    * Changing maps:
        * Best Demo Map: Town10HD (Don't do the Town10 HD OPT)
        * SLC Import Map: compiled_roads

1. Now that the server is running, run the [`run_carla_demo.sh`](./run_carla_demo.sh)
script in this repo in another terminal to run the carla client.
    * [`run_carla_demo.sh`](./run_carla_demo.sh) runs manual control by default. 
        * Note that the client will crash if you do not have a steering wheel connected to the machine when you run the script.
        * You can pass in different arguments to `run_carla_demo.sh` to get different vehicles or charging pad configurations. You essentially pass the name of different csv files in this repo. 
