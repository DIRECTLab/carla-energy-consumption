# Work Notes
## Useful Commands
- lsb_release -a: Tells you what version of Ubuntu you have
- df -h: Checks the space left on the drives
- conda activate *******: Lets you use whatever conda environment you want
- conda deactivate: Shuts down the conda environment that you were using
## Initial Downloading of CARLA
- Followed the Linux build instructions on CARLA documents
- When you reach the "installing Python dependencies" you are going to have deviate a little bit. To be more conscientious, we use the conda environment. Since, we decided to start afresh in downloading CARLA we also created a new conda environment titled `carlaeditorenv`. **When creating a new environment, set Python to 3.8.18 or it will not install the files!** The only install that you have to do using pip is `pip install auditwheel==4.0.0`.
- Used this command to speed up the process: `sudo apt-get install aria2`
- Used this command to clone CARLA repository: `git clone -b ue4-dev https://github.com/carla-simulator/carla`
### Inside CARLA Root Folder
- Fetched latest assets to work using: `./Update.sh`
- Attempted to make Python API, but ran into errors with the <thread> header not existing...
    - First Fix Attempted: include the following code in the .bashrc:
      ```bash
        # Adding clang and clang++ to path
        export CC=/usr/bin/clang
        export CXX=/usr/bin/clang++
      ```
    - Second Fix Attempted: installed labc++-dev libc++abi-dev to try and get C++11 support
      - Used the line command: `sudo apt install libc++-dev libc++abi-dev`
    - Third Fix Attempted: made sure that it truly was clang++ on my end by testing with a file titled test.cpp.
      - This test.cpp file just had the <thread> header and then it checked to see if I could view it.
    - Fourth Fix Attempt: Deleted the entire directory, and conda env and started fresh
      - Same error appeared
    - Fifth Fix Attempt: Chasing down missing files
      - Ran some testing commands and got the following output:
      ```bash
        clang++ -std=c++11 clang_test.cpp -o clang_test -stdlib=libstdc++ -nostdinc++ -isystem /usr/include/c++/11 -isystem /usr/include/x86_64-linux-gnu/c++/7.5 -pthread
        
        In file included from clang_test.cpp:1:
        /usr/include/c++/11/iostream:38:10: fatal error: 'bits/c++config.h' file not found
        #include <bits/c++config.h>
                 ^~~~~~~~~~~~~~~~~~

      ```
    - Sixth Fix Attempt: Github Repository Suggestions by copying my error into Google 
      1. https://github.com/carla-simulator/carla/discussions/8392?sort=top
        - Suggested that I update to Clang 12. Turns out that Ubuntu 22.04 can only run as low as Clang 11, so that's why it keeps breaking. After installing Clang 12 then I was able to compile my test.cpp file; however I got this block of error code now when I try running `make PythonAPI`:
        ```bash
          error: toolset clang-linux initialization:
          error: version '10.0' requested but 'clang++-10.0' not found and version '12.0.1' of default 'clang++' does not match
          error: initialized from
          /home/carla/carla-editor/carla/Build/boost-1.80.0-c10-source/tools/build/src/tools/clang-linux.jam:52: in clang-linux.init from module clang-linux
          /home/carla/carla-editor/carla/Build/boost-1.80.0-c10-source/tools/build/src/build/toolset.jam:44: in toolset.using from module toolset
          /home/carla/carla-editor/carla/Build/boost-1.80.0-c10-source/tools/build/src/tools/clang.jam:33: in clang.init from module clang
          /home/carla/carla-editor/carla/Build/boost-1.80.0-c10-source/tools/build/src/build/toolset.jam:44: in toolset.using from module toolset
          /home/carla/carla-editor/carla/Build/boost-1.80.0-c10-source/tools/build/src/build-system.jam:543: in process-explicit-toolset-requests from module build-system
          /home/carla/carla-editor/carla/Build/boost-1.80.0-c10-source/tools/build/src/build-system.jam:610: in load from module build-system
          /home/carla/carla-editor/carla/Build/boost-1.80.0-c10-source/tools/build/src/kernel/modules.jam:294: in import from module modules
          /home/carla/carla-editor/carla/Build/boost-1.80.0-c10-source/tools/build/src/kernel/bootstrap.jam:135: in module scope from module
        ```
      2. https://github.com/carla-simulator/carla/issues/6901
        - People running into the same problems with clang 10. Some people tried installing Clang 12, but they're getting the same error as listed above.
        - Several comments mentioned installing g++-12. I tried this with Clang12 and still produced the same errors.
    - Final Fix Attempt: Combination of 1 and 2 Github solutions and moving UnRealEngine into new directory CARLA.
      - I uninstalled Clang 12 using the following commands ` sudo apt purge 'clang*'`, `sudo apt autoremove`. I then went to the first Github URL and copied what they suggested doing but replaced 12 with 10. I then installed g++-12 as suggested in the second Github URL. This went further than any previous attempt, but then I came accross this error:

      ```bash
        CMake Error at /opt/cmake-3.28.3-linux-x86_64/share/cmake-3.28/Modules/CMakeDetermineCCompiler.cmake:49 (message):
          Could not find compiler set in environment variable CC:


          /home/carla/CARLA/UnrealEngine_4.26/Engine/Extras/ThirdPartyNotUE/SDKs/HostLinux/Linux_x64/v17_clang-10.0.1-centos7/x86_64-unknown-linux-gnu/bin/clang.
        Call Stack (most recent call first):
          CMakeLists.txt:2 (project)


        CMake Error: CMAKE_C_COMPILER not set, after EnableLanguage
        CMake Error: CMAKE_CXX_COMPILER not set, after EnableLanguage
        -- Configuring incomplete, errors occurred!
        make: *** [Util/BuildTools/Linux.mk:142: setup] Error 1
      ```
      I resolved this problem by putting UnrealEngine_4.26 into a new directory titled "CARLA" because that's what we put in our ~.bashrc file. After I did this I was able to run `make PythonAPI`.


- Attemtped running `make launch` and resulted in this error amoungst all of the warnings and compiling:
  ```bash
      In file included from /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Intermediate/Build/Linux/B4D820EA/UE4Editor/Development/Carla/Module.Carla.3_of_4.cpp:32:
      In file included from /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Vegetation/VegetationManager.cpp:13:
      /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/TaggedComponent.h:7:10: fatal error: 'SplineMeshSceneProxy.h' file not found
      #include "SplineMeshSceneProxy.h"
              ^~~~~~~~~~~~~~~~~~~~~~~~
  ```
  - First Fix Attempt: Probably not the best idea but I'm just going to hardcode the directory path of SplineMeshSceneProxy.h into TaggedComponent.h: `/home/carla/CARLA/UnrealEngine_4.26/Engine/Source/Runtime/Engine/Private/SplineMeshSceneProxy.h`
    - Sounded like a great idea, but it resulted in several different errors:
    ```bash
        In file included from /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Intermediate/Build/Linux/B4D820EA/UE4Editor/Development/Carla/Module.Carla.1_of_4.cpp:27:
        In file included from /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/TaggedComponent.cpp:2:
        /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/TaggedComponent.h:63:44: error: base 'FSplineMeshSceneProxy' is marked 'final'
        class FTaggedSplineMeshSceneProxy : public FSplineMeshSceneProxy
                                                  ^
        /home/carla/CARLA/UnrealEngine_4.26/Engine/Source/Runtime/Engine/Private/SplineMeshSceneProxy.h:78:7: note: 'FSplineMeshSceneProxy' declared here
        class FSplineMeshSceneProxy final : public FStaticMeshSceneProxy
              ^                     ~~~~~
        In file included from /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Intermediate/Build/Linux/B4D820EA/UE4Editor/Development/Carla/Module.Carla.1_of_4.cpp:27:
        In file included from /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/TaggedComponent.cpp:2:
        /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/TaggedComponent.h:69:35: error: 'GetViewRelevance' marked 'override' but does not override any member functions
          virtual FPrimitiveViewRelevance GetViewRelevance(const FSceneView * View) const override;
                                          ^
        In file included from /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Intermediate/Build/Linux/B4D820EA/UE4Editor/Development/Carla/Module.Carla.1_of_4.cpp:27:
        /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/TaggedComponent.cpp:128:12: error: cannot initialize return object of type 'FPrimitiveSceneProxy *' with an rvalue of type 'FTaggedSplineMeshSceneProxy *'
            return new FTaggedSplineMeshSceneProxy(SplineMeshComponent, TaggedMID);
                  ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/TaggedComponent.cpp:254:3: error: type 'FSplineMeshSceneProxy' is not a direct or virtual base of 'FTaggedSplineMeshSceneProxy'
          FSplineMeshSceneProxy(Component)
          ^~~~~~~~~~~~~~~~~~~~~
        /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/TaggedComponent.cpp:259:3: error: use of undeclared identifier 'bVerifyUsedMaterials'
          bVerifyUsedMaterials = false;
          ^
        /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/TaggedComponent.cpp:261:8: error: unknown type name 'FLODInfo'
          for (FLODInfo& LODInfo : LODs) {
              ^
        /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/TaggedComponent.cpp:261:28: error: use of undeclared identifier 'LODs'; did you mean 'LOS'?
          for (FLODInfo& LODInfo : LODs) {
                                  ^~~~
                                  LOS
        /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/V2X/PathLossModel.h:17:5: note: 'LOS' declared here
            LOS,
            ^
        In file included from /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Intermediate/Build/Linux/B4D820EA/UE4Editor/Development/Carla/Module.Carla.1_of_4.cpp:27:
        /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/TaggedComponent.cpp:262:10: error: use of undeclared identifier 'FLODInfo'
            for (FLODInfo::FSectionInfo& SectionInfo : LODInfo.Sections) {
                ^
        /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/TaggedComponent.cpp:270:66: error: call to non-static member function without an object argument
          FPrimitiveViewRelevance ViewRelevance = FSplineMeshSceneProxy::GetViewRelevance(View);
                                                  ~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~
        In file included from /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Intermediate/Build/Linux/B4D820EA/UE4Editor/Development/Carla/Module.Carla.3_of_4.cpp:32:
        In file included from /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Vegetation/VegetationManager.cpp:13:
        /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/TaggedComponent.h:63:44: error: base 'FSplineMeshSceneProxy' is marked 'final'
        class FTaggedSplineMeshSceneProxy : public FSplineMeshSceneProxy
                                                  ^
        /home/carla/CARLA/UnrealEngine_4.26/Engine/Source/Runtime/Engine/Private/SplineMeshSceneProxy.h:78:7: note: 'FSplineMeshSceneProxy' declared here
        class FSplineMeshSceneProxy final : public FStaticMeshSceneProxy
              ^                     ~~~~~
        In file included from /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Intermediate/Build/Linux/B4D820EA/UE4Editor/Development/Carla/Module.Carla.3_of_4.cpp:32:
        In file included from /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Vegetation/VegetationManager.cpp:13:
        /home/carla/carla-editor/carla/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Game/TaggedComponent.h:69:35: error: 'GetViewRelevance' marked 'override' but does not override any member functions
          virtual FPrimitiveViewRelevance GetViewRelevance(const FSceneView * View) const override;
                                          ^
        4 warnings and 2 errors generated.

    ```
    So I removed my hardcoded path directory from TaggedComponent.h
  - Second Fix Attempt: