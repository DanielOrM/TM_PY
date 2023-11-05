#!/bin/bash

source ~/anaconda3/etc/profile.d/conda.sh
conda update conda
if conda info --envs | grep -q tm_env; then echo "Environment already exists"; else conda env create -f -y requirements.yml; fi
eval "$(conda shell.bash hook)"
command -v git >/dev/null 2>&1 ||
{ echo >&2 "Git is not installed. Installing...";
  winget install --id Git.Git -e --source winget
}
conda activate tm_env
python mon_nom_est.py
