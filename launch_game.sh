#!/bin/bash

source ~/anaconda3/etc/profile.d/conda.sh
if conda info --envs | grep -q base; then echo "base already exists"; else conda env create -f -y requirements.yml; fi
conda activate tm_env
python mon_nom_est.py
