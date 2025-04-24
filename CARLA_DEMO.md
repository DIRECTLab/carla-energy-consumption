# Demo Intructions
This readme is meant for when carla demos are to be run at showcases, events, etc. 

First, ensure you have the carla server downloaded onto your machine. If not, you can
clone the repository  found here [carla](https://github.com/carla-simulator/carla/tree/ue4-dev?tab=readme-ov-file).
Make sure to follow their documentation for getting carla setup correctly.

Once you have the carla server setup, run the server

```bash
cd carla
make launch
```

Or if that doesnt work and there is a ./CarlaUE4.sh file run that instead.

This will boot up the carla server. Once it's loaded, the default map should load onto
the screen. Press play to start the server.

Now that the server is running, you can run the following script to run the carla client

```bash
./run_carla.sh
```