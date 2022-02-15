#!/bin/bash
echo "rm -rf /"
echo "Don't run script you have not looked at"
source /home/username/anaconda3/etc/profile.d/conda.sh
conda activate tf15
python3 get_data.py
python3 logic.py


