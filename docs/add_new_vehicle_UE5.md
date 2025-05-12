# Adding a New Vehicle to Carla Unreal Engine 5

## Links
### Reading
* [Carla UE5 Docs](https://carla-ue5.readthedocs.io/en/latest/)

* [CarlaDocs: Content authoring - vehicles](https://carla-ue5.readthedocs.io/en/latest/tuto_content_authoring_vehicles/)


* [CarlaDocs: Generate Detailed Colliders](https://carla-ue5.readthedocs.io/en/latest/tuto_D_generate_colliders/)

### Possibly helpful Videos
* [Import Objects From Blender to Unreal 5](https://youtu.be/BqF5D4kteX8?si=3R2og5zqYq4cYVLL)
* [Rig Blender Vehicle for UE5](https://youtu.be/fcLBQ-zjEK8?si=gr0fc_u_ZLOF5ErP)
---


## Software Requirements
* TODO I used `blender 3.0.1` to add the Kenworth Truck

## Process
* 


## Errors
### Unreal Editor crashes trying to import `KenworthTruck.fbx`
* Crash Report from Unreal Editor
```
LoginId:801c24400ce14c3ab9a8ebfda8e62a7e-000003ee

Assertion failed: ResourceIndex < State.MaxDescriptorCount [File:./Runtime/VulkanRHI/Private/VulkanDescriptorSets.cpp] [Line: 890] 
You need to grow the resource array size for [VK_DESCRIPTOR_TYPE_UNIFORM_TEXEL_BUFFER]!


libUnrealEditor-VulkanRHI.so!FVulkanBindlessDescriptorManager::GetFreeResourceIndex(FVulkanBindlessDescriptorManager::BindlessSetState&) [/home/carla/UnrealEngine5_carla/Engine/Source/./Runtime/VulkanRHI/Private/VulkanDescriptorSets.cpp:890]
libUnrealEditor-VulkanRHI.so!FVulkanBindlessDescriptorManager::ReserveDescriptor(VkDescriptorType) [/home/carla/UnrealEngine5_carla/Engine/Source/./Runtime/VulkanRHI/Private/VulkanDescriptorSets.cpp:693]
libUnrealEditor-VulkanRHI.so!FVulkanShaderResourceView::FVulkanShaderResourceView(FRHICommandListBase&, FVulkanDevice&, FRHIViewableResource*, FRHIViewDesc const&) [/home/carla/UnrealEngine5_carla/Engine/Source/./Runtime/VulkanRHI/Private/VulkanUAV.cpp:13]
libUnrealEditor-VulkanRHI.so!FVulkanDynamicRHI::RHICreateShaderResourceView(FRHICommandListBase&, FRHIViewableResource*, FRHIViewDesc const&) [/home/carla/UnrealEngine5_carla/Engine/Source/./Runtime/VulkanRHI/Private/VulkanUAV.cpp:674]
libUnrealEditor-Engine.so!FStaticMeshVertexBuffer::InitRHI(FRHICommandListBase&) [/home/carla/UnrealEngine5_carla/Engine/Source/Runtime/RHI/Public/RHICommandList.h:886]
libUnrealEditor-RenderCore.so!FRenderResource::InitResource(FRHICommandListBase&) [/home/carla/UnrealEngine5_carla/Engine/Source/./Runtime/RenderCore/Private/RenderResource.cpp:190]
libUnrealEditor-Engine.so!FStaticMeshVertexBuffer::InitResource(FRHICommandListBase&) [/home/carla/UnrealEngine5_carla/Engine/Source/./Runtime/Engine/Private/Rendering/StaticMeshVertexBuffer.cpp:343]
libUnrealEditor-Engine.so!FStaticMeshVertexBuffers::InitFromDynamicVertex(FRHICommandListBase*, FRenderCommandPipe*, FLocalVertexFactory*, TArray<FDynamicMeshVertex, TSizedDefaultAllocator<32> >&, unsigned int, unsigned int)::$_0::operator()(FRHICommandListBase&) const [/home/carla/UnrealEngine5_carla/Engine/Source/./Runtime/Engine/Private/StaticMesh.cpp:1103]
libUnrealEditor-RenderCore.so!UE::Core::Private::Function::TFunctionRefCaller<FRenderThreadCommandPipe::EnqueueAndLaunch(char16_t const*, unsigned int&, TStatId, TUniqueFunction<void (FRHICommandListImmediate&)>&&)::$_0, void>::Call(void*) [/home/carla/UnrealEngine5_carla/Engine/Source/Runtime/Core/Public/Templates/Function.h:470]
libUnrealEditor-RenderCore.so!TGraphTask<TFunctionGraphTaskImpl<void (), (ESubsequentsMode::Type)1> >::ExecuteTask() [/home/carla/UnrealEngine5_carla/Engine/Source/Runtime/Core/Public/Templates/Function.h:470]
libUnrealEditor-Core.so!UE::Tasks::Private::FTaskBase::TryExecuteTask() [/home/carla/UnrealEngine5_carla/Engine/Source/Runtime/Core/Public/Tasks/TaskPrivate.h:504]
libUnrealEditor-Core.so!FNamedTaskThread::ProcessTasksNamedThread(int, bool) [/home/carla/UnrealEngine5_carla/Engine/Source/Runtime/Core/Public/Async/TaskGraphInterfaces.h:482]
libUnrealEditor-Core.so!FNamedTaskThread::ProcessTasksUntilQuit(int) [/home/carla/UnrealEngine5_carla/Engine/Source/./Runtime/Core/Private/Async/TaskGraph.cpp:667]
libUnrealEditor-RenderCore.so!RenderingThreadMain(FEvent*) [/home/carla/UnrealEngine5_carla/Engine/Source/./Runtime/RenderCore/Private/RenderingThread.cpp:317]
libUnrealEditor-RenderCore.so!FRenderingThread::Run() [/home/carla/UnrealEngine5_carla/Engine/Source/./Runtime/RenderCore/Private/RenderingThread.cpp:468]
libUnrealEditor-Core.so!FRunnableThreadPThread::Run() [/home/carla/UnrealEngine5_carla/Engine/Source/./Runtime/Core/Private/HAL/PThreadRunnableThread.cpp:25]
libUnrealEditor-Core.so!FRunnableThreadPThread::_ThreadProc(void*) [/home/carla/UnrealEngine5_carla/Engine/Source/Runtime/Core/Private/HAL/PThreadRunnableThread.h:187]
libc.so.6!UnknownFunction(0x94ac2)
libc.so.6!UnknownFunction(0x12684f)
```

* [Forum on similar issue](https://forums.unrealengine.com/t/ue5-2-freezes-on-importing-fbx/1263565/2?page=2)
* I tested importing a very simple FBX of just the default cube on Blender startup. This did work. The issue seems to be with the kenworth FBX file specifically.

#### Attempted Fixes
1. Stuff I am reading with chatGPT saying that the issue could be with the Nvidia and Vulkan drivers. Which the one recommended by `sudo ubuntu-drivers devices` is newer than the one being used on this machine.
    * Updated nvidia to `driver   : nvidia-driver-570 - third-party non-free recommended`
    * No change, still same error upon attempt to import.

2. Loaded the original FBX file into Blender. Tried adding a "decimate" modifier to the truck in Blender, which was supposed to simplify it. Then exported it again.
    * Changed ratio to `0.75`
    * Did the `triangulate` option which makes all mesh shapes triangles to simplify as well.
    * Still failed to import.

3. Tried exporting it with those changes again, but looked closer at the settings of the export. Not sure what I changed, but the truck still looked pretty good, and this time the exported FBX is much smaller than the original, it is `20Kb`, instead of the original FBX file which is `40Mb`.

4. `[2025.05.08-22.42.18:716][722]r.GpuProfilerMaxEventBufferSizeKB = "1024"` ran this in the Unreal Console to increase the buffer size.
    * Still failing. I am thinking maybe I need to look more into the import settings for bringing in the file, I might be doing something wrong.

5. Ran `sudo apt install vulkan-tools libvulkan1`
    * Console said they were already at the latest version.
    * Tried again, still the same error.

6. Editting file in Carla UE5 source code to increase the size of the buffer
    * I modified line 890 to be the following (just added more text to see what the size of `State.MaxDescriptorCount` actually is)
    * `checkf(ResourceIndex < State.MaxDescriptorCount, TEXT("You need to grow the resource array size for [%s]! State.MaxDescriptoCount=%dDONUT"), VK_TYPE_TO_STRING(VkDescriptorType, State.Descri    ptorType), State.MaxDescriptorCount);`

* ls /etc/vulkan/icd.d/

Check in that directory. Sitll having issues. Even though the fbx is much smaller. Either I am importing/exporting badly. Or maybe vulkan driver issues.
Maybe increase vulkan buffer size?

#### Fixed

---