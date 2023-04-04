#!/bin/bash
source /root/miniconda3/etc/profile.d/conda.sh
conda activate tf15
python3 /srv/dev-disk-by-uuid-14c64766-d1ce-46c9-82f7-d1e8b371d1cb/nas/Projects/lol_predictions/get_data.py
if [ $1 ]; then
    if ! python3 /srv/dev-disk-by-uuid-14c64766-d1ce-46c9-82f7-d1e8b371d1cb/nas/Projects/lol_predictions/logic.py $1 $2 $3 $4 $5 $6; then
        exit 1
    fi
else
    if ! python3 /srv/dev-disk-by-uuid-14c64766-d1ce-46c9-82f7-d1e8b371d1cb/nas/Projects/lol_predictions/logic.py; then
        exit 1
    fi
fi






