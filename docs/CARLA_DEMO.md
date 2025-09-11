# Demo Intructions
*How to run carlaUE4 for demos at showcases, events, etc.* 

1. Ensure you have the carla server downloaded and setup on your machine. 
    * You can clone the repository here: [carla repo](https://github.com/carla-simulator/carla/tree/ue4-dev?tab=readme-ov-file).
    * Make sure to follow their [documentation](https://carla.readthedocs.io/en/latest/) for getting carla setup correctly.
    * Other Helpful Docs for setup and configurations
        * [`carla_startup.md`](./carla_install_help.md)
        * [`CARLA_editor_notes_Zac.md`](./CARLA_editor_notes_Zac.md)
        * [`create_world.md`](./create_world.md)
        * [`add_new_vehicle.md`](./add_new_vehicle.md)
        * [`steering_wheel_manual.md`](./steering_wheel_manual.md)

2. Starting the Carla Server
    1. Open a terminal
    2. Activate the server conda env: `carla-editor-env`
        * Run `conda env list` to see all available conda envs
    3. Move into the `carla` directory
    4. Run `make launch`
    * This will start up the Carla Server.

3. Once the carla server is loaded, press play button in the Unreal Editor to
start the server.

4. Now that the server is running, run the [`run_carla.sh`](./run_carla.sh)
script in this repo in another terminal to run the carla client.
    * [`run_carla.sh`](./run_carla.sh) runs manual control by default. The 
    client will crash if you do not have a steering wheel connected
    to the machine when you run the script.
    * You can edit the parameters in the client script to get different vehicles 
    or charging pad configurations. You pass it different csv files essentially.