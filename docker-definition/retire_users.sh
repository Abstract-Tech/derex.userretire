#!/bin/sh
COOL_OFF_DAYS=${COOL_OFF_DAYS:-0}

/tubular/scripts/get_learners_to_retire.py --config_file /config.yaml --output_dir /users --cool_off_days ${COOL_OFF_DAYS}
for file in $(find /users -type f); do
    source $file
    /tubular/scripts/retire_one_learner.py --config_file /config.yaml --username=${RETIREMENT_USERNAME}
    rm $file
done
