#!/bin/bash
# This is for hw1 of gameAI 
# Some levels need specified "frame" to play, otherwise it delays


# Check to make sure the user has entered exactly three arguments
if [ $# -ne 0 ]
then 
    echo -e "Usage: ./commandAuto.sh"
    exit 1
fi


for level in {1..24}; do
    if [ $level -eq 8 ] || [ $level -eq 9 ] || [ $level -eq 11 ] || [ $level -eq 13 ] || [ $level -eq 15 ] || [ $level -eq 16 ] || [ $level -eq 17 ] || [ $level -eq 21 ] || [ $level -eq 22 ] || [ $level -eq 23 ]
    then    
        python_option="-m mlgame -f 20 --one-shot -i /Users/harris/MLGame/arkanoid/ml/ml_play_model.py . --difficulty NORMAL --level $level"
    else
        python_option="-m mlgame -f 120 --one-shot -i /Users/harris/MLGame/arkanoid/ml/ml_play_model.py . --difficulty NORMAL --level $level"
    fi 

    echo "Running command with level $level"
    $(which python) $python_option  
  
    # Get the process ID of the last backgrounded process
    pid=$!

    # Wait for the process to finish
    wait $pid

done


