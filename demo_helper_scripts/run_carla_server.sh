#!/bin/bash
eval "$(conda shell.bash hook)"

conda activate carlaenv

cd ~/carla

make launch