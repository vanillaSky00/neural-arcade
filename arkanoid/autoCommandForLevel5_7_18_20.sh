#!/bin/bash
# This is for hw1 of gameAI 
# Some levels need specified "frame" to play, otherwise it delays


# Check to make sure the user has entered exactly three arguments
if [ $# -ne 0 ]
then 
    echo -e "Usage: ./commandAuto.sh"
    exit 1
fi


for level in {5,7,18,20}; do
        python_option="-m mlgame -f 20 --one-shot -i /Users/harris/MLGame/arkanoid/ml/ml_play_model.py . --difficulty NORMAL --level $level"

    echo "Running command with level $level"
    $(which python) $python_option  
  
    # Get the process ID of the last backgrounded process
    pid=$!

    # Wait for the process to finish
    wait $pid

done


