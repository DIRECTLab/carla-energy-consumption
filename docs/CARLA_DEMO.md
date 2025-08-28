# Demo Intructions
*How to run carlaUE4 for demos at showcases, events, etc.* 

1. Ensure you have the carla server downloaded and setup on your machine. 
    * You can clone the repository here: [carla repo](https://github.com/carla-simulator/carla/tree/ue4-dev?tab=readme-ov-file).
    * Make sure to follow their [documentation](https://carla.readthedocs.io/en/latest/) for getting carla setup correctly.
    * Other Helpful Docs for setup and configurations
        * [`carla_startup.md`](./carla_startup.md)
        * [`CARLA_editor_notes_Zac.md`](./CARLA_editor_notes_Zac.md)
        * [`create_world.md`](./create_world.md)
        * [`add_new_vehicle.md`](./add_new_vehicle.md)
        * [`steering_wheel_manual.md`](./steering_wheel_manual.md)

2. Once you have the carla server setup, run the server
    ```bash
    cd carla
    make launch
    ``` 
    * This will boot up the carla server.
    * If that doesnt work and there is a `./CarlaUE4.sh` file run that 
    instead.

3. Once the carla server is loaded, the default map should load onto the screen.
Press the play to start the server.

4. Now that the server is running, run the [`run_carla.sh`](./run_carla.sh)
script in this repo in another terminal to run the carla client.
    * [`run_carla.sh`](./run_carla.sh) runs the manual control by default. The 
    client will not crash if you do not have a steering wheel connected
    to the machine.
    * You can edit the parameters in the client script to get different vehicles 
    or charging pad configurations. You pass it different csv files essentially.