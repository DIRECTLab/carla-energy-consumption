# How to Install CARLA 0.9.14 with Unreal Engine Editor
## Process
0. CARLA must be installed from the source to allow editing abilities. The 
following was done with CARLA installed from source for Linux on Ubuntu 20. 
Go [here](https://carla.readthedocs.io/en/latest/build_linux/) for how to build 
from source in Linux. After making sure you have all of the correct requirements,
make sure that when you are cloning CARLA that you are 
getting version 0.9.14. Use the following command after downloading aria2:
`git clone -b 0.9.14 https://github.com/carla-simulator/carla.git`.
0. After cloning CARLA, you need to have the assets specific to CARLA 0.9.14.
This requires that you go into the Update.sh and replacing the URL on the 50th line
with this URL: `https://carla-assets.s3.us-east-005.backblazeb2.com/${CONTENT_ID}.tar.gz`
0. You are then going to run `make PythonAPI`. The first time probably won't work
due to the boost file. You are going to have to download it yourself and placing it into
the Build file in VScode. You can find the correct boost file by going to the following URL:
`https://www.boost.org/users/history/version_1_80_0.html`. **Make sure that you delete the 
"bad" boost file before putting in your downloaded boost!** You will know the
boost file is bad if you open it and you are able to read text in your text editor.
It won't recognize the boost you downloaded unless you do it otherwise. 
You will likely have to do this process every time that you run `make ...`
0. Run `make launch`
0. The CARLA server with the Unreal Engine Editor should pop up and you're good to go!