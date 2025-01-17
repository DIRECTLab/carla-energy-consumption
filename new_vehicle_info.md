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

0. CARLA must be installed from the source to allow editing abilities. The 
following was done with CARLA installed from source for Linux on Ubuntu 20. 
Go [here](https://carla.readthedocs.io/en/latest/build_linux/) for how to build 
from source in Linux. Make sure that when you are cloning CARLA that you are 
getting version 0.9.14. use the command 
`git clone -b 0.9.14 https://github.com/carla-simulator/carla.git`. 
When pip installing the carla package install the correct package 
`pip install carla==0.9.14`
1. Download and install [Blender](https://www.blender.org/download/)
2. Find an .fbx model of the desired vehicle
    - as of right now I have found that it is not necessary to get a rigged 
    3D model for the wheels to move as part of the importing process is 
    connecting your choice of model to the bones of a rigged model which will 
    allow the wheels to move.
3. Export a .fbx model of a vehicle from CARLA to use as a blueprint
    - run CARLA using the `make launch` command
    - In the content browser navigate to the folder 
    Content/Carla/Static/Car/4Wheeled/
    - Select the desired vehicle folder - I used Tesla
    - Choose the main blueprint that contains the entire vehicle - for Tesla 
    the file was called SM_TeslaM3_v2. You could probably use the blueprint 
    from the `Content/Carla/Blueprints/Vehicles/[vehicle_folder]` but it will 
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
in your final result in CARLA. Then continue following the video
11. When importing in CARLA make sure the wheels are spheres and that they come 
outside the body of the truck, otherwise the wheels will spin wrong or they will 
spin and not move the truck at all.

12. It's important to note that the CARLA simulator is meant for vehicles with 
4 wheels. When trying to add a vehicle with more than 4 wheels, you need to 
remove the vertex groups in blender that don't pertain to the 4 wheels you want 
to move in the CARLA simulator. Otherwise the physics will not work correctly.


## Notes
Step 12 pertains mostly to the problems I had while trying to import the 
Kenworth truck. I got it working in the simulator ONLY after removing any 
reference whatsoever to the middle left and middle right wheels. 
The KenworthTruck.fbx file in this folder should work straight out of the box, 
which means you can start 
[this tutorial](https://www.youtube.com/watch?v=0F3ugwkISGk&t=1027s) at 11:41 
and go from there.

Also, if you add a new vehicle and the wheels fall through the ground, make sure
that in the FrontWheel and RearWheel blueprints that the shape is not cylinder
but rather wheel_shape and that the Tire config is commontireconfig.