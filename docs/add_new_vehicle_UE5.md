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

* 2nd attempt exporting then importing again
```
LoginId:801c24400ce14c3ab9a8ebfda8e62a7e-000003ee

Assertion failed: ResourceIndex < State.MaxDescriptorCount [File:./Runtime/VulkanRHI/Private/VulkanDescriptorSets.cpp] [Line: 890] 
You need to grow the resource array size for [VK_DESCRIPTOR_TYPE_UNIFORM_TEXEL_BUFFER]!


libUnrealEditor-VulkanRHI.so!FVulkanBindlessDescriptorManager::GetFreeResourceIndex(FVulkanBindlessDescriptorManager::BindlessSetState&) [/home/carla/UnrealEngine5_carla/Engine/Source/./Runtime/VulkanRHI/Private/VulkanDescriptorSets.cpp:890]
libUnrealEditor-VulkanRHI.so!FVulkanBindlessDescriptorManager::ReserveDescriptor(VkDescriptorType) [/home/carla/UnrealEngine5_carla/Engine/Source/./Runtime/VulkanRHI/Private/VulkanDescriptorSets.cpp:693]
libUnrealEditor-VulkanRHI.so!FVulkanShaderResourceView::FVulkanShaderResourceView(FRHICommandListBase&, FVulkanDevice&, FRHIViewableResource*, FRHIViewDesc const&) [/home/carla/UnrealEngine5_carla/Engine/Source/./Runtime/VulkanRHI/Private/VulkanUAV.cpp:13]
libUnrealEditor-VulkanRHI.so!FVulkanDynamicRHI::RHICreateShaderResourceView(FRHICommandListBase&, FRHIViewableResource*, FRHIViewDesc const&) [/home/carla/UnrealEngine5_carla/Engine/Source/./Runtime/VulkanRHI/Private/VulkanUAV.cpp:674]
libUnrealEditor-Engine.so!FColorVertexBuffer::InitRHI(FRHICommandListBase&) [/home/carla/UnrealEngine5_carla/Engine/Source/Runtime/RHI/Public/RHICommandList.h:886]
libUnrealEditor-RenderCore.so!FRenderResource::InitResource(FRHICommandListBase&) [/home/carla/UnrealEngine5_carla/Engine/Source/./Runtime/RenderCore/Private/RenderResource.cpp:190]
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

* Stuff I am reading with chatGPT saying that the issue could be with the Nvidia and Vulkan drivers. Which the oen recommended by `sudo ubuntu-drivers devices` is newer than the one being used on this machine.

* Going to update to `driver   : nvidia-driver-570 - third-party non-free recommended` this driver.

* Current Driver
```bash
(base) carla@gaston-System-Product-Name:~$ nvidia-smi
Thu May  8 13:58:42 2025
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 560.28.03              Driver Version: 560.28.03      CUDA Version: 12.6     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 3090        Off |   00000000:01:00.0  On |                  N/A |
|  0%   50C    P8             43W /  370W |    6732MiB /  24576MiB |     15%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A      2744      G   /usr/lib/xorg/Xorg                            323MiB |
|    0   N/A  N/A      2891      G   /usr/bin/gnome-shell                           86MiB |
|    0   N/A  N/A      3506      G   /opt/google/chrome/chrome                       4MiB |
|    0   N/A  N/A      3554      G   ...seed-version=20250508-050101.681000         98MiB |
|    0   N/A  N/A      8867      G   ...erProcess --variations-seed-version         56MiB |
|    0   N/A  N/A     29389    C+G   .../Engine/Binaries/Linux/UnrealEditor       6021MiB |
+-----------------------------------------------------------------------------------------+
```

* Currently Available drivers
```bash
(base) carla@gaston-System-Product-Name:~$ sudo ubuntu-drivers devices
== /sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0 ==
modalias : pci:v000010DEd00002204sv00001462sd00003884bc03sc00i00
vendor   : NVIDIA Corporation
model    : GA102 [GeForce RTX 3090]
driver   : nvidia-driver-545-open - distro non-free
driver   : nvidia-driver-565 - third-party non-free
driver   : nvidia-driver-535-open - distro non-free
driver   : nvidia-driver-570-server - distro non-free
driver   : nvidia-driver-560-open - third-party non-free
driver   : nvidia-driver-545 - distro non-free
driver   : nvidia-driver-550 - distro non-free
driver   : nvidia-driver-535 - distro non-free
driver   : nvidia-driver-570 - third-party non-free recommended
driver   : nvidia-driver-470-server - distro non-free
driver   : nvidia-driver-535-server-open - distro non-free
driver   : nvidia-driver-565-open - third-party non-free
driver   : nvidia-driver-570-open - third-party non-free
driver   : nvidia-driver-560 - third-party non-free
driver   : nvidia-driver-550-open - distro non-free
driver   : nvidia-driver-470 - distro non-free
driver   : nvidia-driver-570-server-open - distro non-free
driver   : nvidia-driver-535-server - distro non-free
driver   : xserver-xorg-video-nouveau - distro free builtin
```