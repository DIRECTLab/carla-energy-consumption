# Adding a New Vehicle to CARLA
[This](https://carla.readthedocs.io/en/latest/tuto_content_authoring_vehicles/) 
is the link to the documentation about importing an fbx file into CARLA for a 
new vehicle.

go [here](https://www.youtube.com/watch?v=0F3ugwkISGk) for the youtube tutorial

go [here](https://forums.unrealengine.com/t/export-fbx-from-ue4/374740/2) for 
how to export the fbx file from CARLA

Don't forget to remove the extra stuff from the blender file.
I don't think we need a fancy fbx model that moves. You add the moving wheels 
seperately. Though it might be useful for how the trailer moves behind the 
cab...hmmm

1. Download and install [Blender](https://www.blender.org/download/)
2. Find an .fbx model of the desired vehicle
    - as of right now I have found that it is not necessary to get a rigged 
    3D model for the wheels to move as part of the importing process is 
    connecting your choice of model to the bones of a rigged model which will 
    allow the wheels to move.
3. Export a .fbx model of a vehicle from CARLA to use as a blueprint
    - run CARLA using the `make launch` command
    - In the content browser navigate to the folder 
    `Content/Carla/Static/Car/4Wheeled/`
    - Select the desired vehicle folder - I used Tesla
    - Choose the main blueprint that contains the entire vehicle - for Tesla 
    the file was called SM_TeslaM3_v2. You could probably use the blueprint 
    from the `Content/Carla/Static/Car/4Wheeled/[vehicle_folder]` but it will 
    have extra stuff in it to deal with and the first suggested one is closest 
    to what will be seen in the tutorial below. 
    - drag your chosen blueprint into the scene
    - click on the vehicle
    - go to `File` at the top and choose `Export Selected`
    - choose where you want to download to, name the file, and be sure that 
    the selected file type is .fbx
    - use the default export settings
4. Open a new Blender project
5. Delete the automatically generated objects
6. Go to `File` and select `Import` and import the .fbx file that you exported 
from CARLA'
7. Hide the 3 extra meshes that it generates that show the same thing as the 
first one.
8. Import the .fbx file you downloaded of the new vehicles your are adding 
into a new collection (the video will show you)
9. Follow along with this [video](https://www.youtube.com/watch?v=0F3ugwkISGk) 
to connect the bones of the blueprint to your new vehicle. Refer to step 10 
before following the video instructions to export from Blender
- When the video goes to `Content/Carla/Static/Static/...` in the updated 
    version of CARLA this path is `Content/Carla/Static/Car/4Wheeled`
- The link to the documentation the video refers to is in the video 
    description, when going there make sure you are on the right page for your 
    version of CARLA.
10. Before exporting delete the hidden extra meshes or else they will show up 
in your final result in CARLA. It's important to note that the CARLA simulator is meant for vehicles with 
4 wheels. When trying to add a vehicle with more than 4 wheels, you need to 
remove the vertex groups in blender that don't pertain to the 4 wheels you want 
to move in the CARLA simulator. Otherwise the physics will not work correctly. Then continue following the video 
11. When importing into UE4, go to `Content/Carla/Static/Car/4Wheeled/[vehicle_folder]` and import with the default settings.
12. Click on the PhysicsAssest file. The video walks you through this pretty well, but just a couple of things to take note on:
- To make more realistic, click on the `Vehicle_Base` and look at the Details panel. You should see a Physics section with 
  `MassinKg` option. Check this option and put a rough estimate of how much your vehicle weights (look up on Google).
- Also make sure that your Vehicle_Base is a capsule base if you don't have a `SMC_<vehicle_name>` file. 
  If you need to switch out the shape, then right-click on the `Vehicle_Base` and click on `Add Capsule` under `Add Shape`.
  If you do have a `SMC_<vehicle_name>` file, then right-click on the `Vehicle_Base`, click on `Copy Collision from StaticMesh`
  and then select your SMC file.
- Make sure that your tires are outside of the capsule or the vehicle's physics will be messed up.
13. When you get to the tire configuration in the video, you should make sure that in the FrontWheel and RearWheel blueprints
the shape is not cylinder but rather wheel_shape and that the Tire config is commontireconfig. This will prevent
your tires from sinking into the ground.
14. After completing the video and you want to test out the vehicle follow these steps:
- In the UE4, hit `Play` on the top of your screen. This starts the server.
- In another terminal, cd into `~/carla/PythonAPI/examples`
- Run this command: `python3 manual_control.py --filter <make or model that you listed in the vehicle factory>`
- You may have to cycle through a few vehicles if its a common make like tesla or ford. You can do this
  by hitting the backspace.
- This is a great place to test out your new vehicle to make sure the tires aren't stuck in the ground, and the vehicle
  handles as you expect.
15. Once you satisfied with the changes you have made, you need to make it a vehicle that we can drive with the steering wheel.
- First go to the `input/examples` folder in `CARLA-ENGERGY-CONSUMPTION`. Copy the `kenworth.csv` file, but change the name of the file and change `vehicle.kenworth.t860e` into `vehicle.<make of your vehicle>.<model of your vehicle>`. In the Make/Modle sections, put the same labels that you put in the Vehicle Factory for your vehicle. Notice, that everything has to be lowercase even if you captilized it in the Vehicle Factory.
- Update `run_carla_demo.sh` by going to the line that runs manual_control_steeringwheel and replace the vehicle.csv file with the .csv file that you
just created. If everything was done correctly, then you should be able to type `run_carla_demo.sh` in the terminal and it will run the client side
and upload your new vehicle to test in the simulation. 



## Notes
Step 12 pertains mostly to the problems I had while trying to import the 
Kenworth truck. I got it working in the simulator ONLY after removing any 
reference whatsoever to the middle left and middle right wheels. 
The KenworthTruck.fbx file in this folder should work straight out of the box, 
which means you can start 
[this tutorial](https://www.youtube.com/watch?v=0F3ugwkISGk&t=1027s) at 11:41 
and go from there.

There is a new feature in the documentation about adding an N wheeled vehicle.
This may be useful when adding a trailer to the truck.