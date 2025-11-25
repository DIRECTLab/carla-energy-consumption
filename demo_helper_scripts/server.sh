#!/bin/bash
eval "$(conda shell.bash hook)"

export UE4_ROOT=$HOME/UnrealEngine_4.26

conda activate carlaenv

cd $HOME/carla

make launch
