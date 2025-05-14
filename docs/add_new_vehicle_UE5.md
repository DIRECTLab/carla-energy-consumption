# Adding a New Vehicle to Carla Unreal Engine 5

## Links
TODO clean these links up, delete non-useful ones  
Reading
* [Carla UE5 Docs](https://carla-ue5.readthedocs.io/en/latest/)

* [CarlaDocs: Content authoring - vehicles](https://carla-ue5.readthedocs.io/en/latest/tuto_content_authoring_vehicles/)

* [CarlaDocs: Generate Detailed Colliders](https://carla-ue5.readthedocs.io/en/latest/tuto_D_generate_colliders/)

Possibly helpful Videos
* [Import Objects From Blender to Unreal 5](https://youtu.be/BqF5D4kteX8?si=3R2og5zqYq4cYVLL)
* [Rig Blender Vehicle for UE5](https://youtu.be/fcLBQ-zjEK8?si=gr0fc_u_ZLOF5ErP)
* [UE4 Adding Trailer to Vehicle](https://www.youtube.com/watch?v=mJufrK7RkeI)
* [UE4 Add vehicle to Carla](https://www.youtube.com/watch?v=0F3ugwkISGk)
---


## Software Requirements
* TODO I used `blender 3.0.1` to add the Kenworth Truck

## Process
* TODO

## Status
* Vehicles is imported and supposedly setup? I went through all of the adding vehicle docs, but it seems incomplete, I still do not know how to get the kenworth driving, not just sitting static on the map.

## Errors
### Unreal Editor crashes trying to import `KenworthTruck.fbx`
* Crash Report from Unreal Editor
    ```
    LoginId:801c24400ce14c3ab9a8ebfda8e62a7e-000003ee

    Assertion failed: ResourceIndex < State.MaxDescriptorCount [File:./Runtime/VulkanRHI/Private/VulkanDescriptorSets.cpp] [Line: 890] 
    You need to grow the resource array size for [VK_DESCRIPTOR_TYPE_UNIFORM_TEXEL_BUFFER]!
    ```

* [Forum on similar issue](https://forums.unrealengine.com/t/ue5-2-freezes-on-importing-fbx/1263565/2?page=2)
* I tested importing a very simple FBX of just the default cube on Blender startup. This did work. The issue seems to be with the kenworth FBX file specifically.

#### Attempted Fixes
1. Stuff I am reading with chatGPT saying that the issue could be with the Nvidia and Vulkan drivers. Which the one recommended by `sudo ubuntu-drivers devices` is newer than the one being used on this machine.
    * Updated nvidia to `driver   : nvidia-driver-570 - third-party non-free recommended`
    * No change, still same error upon attempt to import.
    ---     
2. Loaded the original FBX file into Blender. Tried adding a "decimate" modifier to the truck in Blender, which was supposed to simplify it. Then exported it again.
    * Changed ratio to `0.75`
    * Did the `triangulate` option which makes all mesh shapes triangles to simplify as well.
    * Still failed to import.
    ---

3. Tried exporting it with those changes again, but looked closer at the settings of the export. 
    * Not sure what I changed, but the truck still looked pretty good, and this time the exported FBX is much smaller than the original, it is `20Kb`, instead of the original FBX file which is `40Mb`.
    ---
    
4. `[2025.05.08-22.42.18:716][722]r.GpuProfilerMaxEventBufferSizeKB = "1024"` ran this in the Unreal Console to increase the buffer size.
    * Still failing. I am thinking maybe I need to look more into the import settings for bringing in the file, I might be doing something wrong.
    ---  

5. Ran `sudo apt install vulkan-tools libvulkan1`
    * Console said they were already at the latest version.
    * Tried again, still the same error.
    ---

6. Editting file in Carla UE5 source code to increase the size of the buffer
    * I modified line 890 to be the following (just added more text to see what the size of `State.MaxDescriptorCount` actually is)
    * `checkf(ResourceIndex < State.MaxDescriptorCount, TEXT("You need to grow the resource array size for [%s]! State.MaxDescriptoCount=%d"), VK_TYPE_TO_STRING(VkDescriptorType, State.Descri    ptorType), State.MaxDescriptorCount);`
    * Result: `You need to grow the resource array size for [VK_DESCRIPTOR_TYPE_UNIFORM_TEXEL_BUFFER]! curr_size=65536`. I did not find a way to actually increase the buffer size. Also I am giving up on this as I think this will not actually be a good fix.
    ---

7. Tried importing Kenworth truck without the material
    * Imported as `FBX skeletal meshes` file type.  
    ![screenshot UE5 import settings](../images/UE5_material_import_settings.png)
    *Settings to exclude materials in the import.*
    * I kept the other settings as the defaults.
    * I even undid the decimate modifier to unsimplify the truck and it imported fine as long as I did not include the material.
    * I also tried it including the textures and the import still worked.
    * Result: This import worked! It brought in the truck.  
        * The issue is specifically with the truck material, possible being too complex or my thought is that it is in some format not compatible with UE5.
    ---

8. Deleted some materials that did not seem to be used for much
    * I deleted down to 6 materials
    * Result: I was able to import the truck and it's materials!

#### Fixed
Deleting the materials worked. I have the Kenworth Truck imported.
* It seems that the kenworth truck FBX had a lot of different materials compared to the vehicles in carla which had around 6, give or take a few. I believe that ws the issue, just too many materials.
* Later I also found that Carla includes some basic vehicle materials which can be used on added vehicles, I switched most of the Kenworths used materials to be these as they honestly look nicer than the ones I imported.
