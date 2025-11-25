# How to Install CARLA 0.9.14 with Unreal Engine Editor

1. CARLA must be built from source to allow editing abilities. The following was done with CARLA installed from source for Linux on Ubuntu 20. Go to [CARLA documentation v0.9.14](https://carla.readthedocs.io/en/0.9.14/build_linux/) for instructions on how to build from source in Linux. After making sure you have all of the correct requirements, make sure that when you are cloning CARLA that you are getting `v0.9.14`. Use the following command after downloading `aria2`: `git clone -b 0.9.14 https://github.com/carla-simulator/carla.git`.

1. After cloning CARLA, you need to have the assets specific to CARLA 0.9.14. This requires that you go into the `Update.sh` and replace the URL on line 50 with this URL: `https://carla-assets.s3.us-east-005.backblazeb2.com/${CONTENT_ID}.tar.gz`

1. Run `make PythonAPI` 
    * The first time probably won't work due to the boost file. You are going to have to download it manually and place it into `carla/Build/` (`carla` or whatever you named the root directory of the server repo that you cloned, default name is `carla`).  
    * You can find the correct boost file by going to the [Boost v1.80.0 release page](https://www.boost.org/releases/1.80.0/). You want to download `boost_1_80_0.tar.gz`, place this file into the directory. 
        * **Make sure that you delete the "bad" boost file before putting in your downloaded boost!** You will know the boost file is bad if you open it and you are not able to read text in your text editor. It won't recognize the boost you downloaded unless you do it otherwise.

1. Run `make launch`

1. The CARLA server with the Unreal Engine Editor should pop up and you're good to go!