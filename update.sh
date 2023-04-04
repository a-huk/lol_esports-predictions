#!/bin/bash
python3 /srv/dev-disk-by-uuid-14c64766-d1ce-46c9-82f7-d1e8b371d1cb/nas/Projects/lol_predictions/updater.py >> /srv/dev-disk-by-uuid-14c64766-d1ce-46c9-82f7-d1e8b371d1cb/nas/Projects/lol_predictions/log.txt
cd /srv/dev-disk-by-uuid-14c64766-d1ce-46c9-82f7-d1e8b371d1cb/nas/Projects/lol_predictions/lol_esports-predictions/ && git config --global user.name "ahBot" && git config --global user.email "huk.adam.g@gmail.com" && git add * && git commit -m 'Update predictions' && git push origin
