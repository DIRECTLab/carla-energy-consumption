#!/bin/bash
eval "$(conda shell.bash hook)"

conda activate carlaenv

cd $HOME/my-carla/LinuxNoEditor

./CarlaUE4.sh -carla-rpc-port=2000
