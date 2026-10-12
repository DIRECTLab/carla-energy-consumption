#!/bin/bash
eval "$(conda shell.bash hook)"

conda activate carlaenv

cd $HOME/carla/Unreal/CarlaUE4/Saved/StagedBuilds/LinuxNoEditor

./CarlaUE4.sh -carla-rpc-port=2000
