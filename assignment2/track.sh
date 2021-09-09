#!/bin/bash -x

# Declare functions
# The track function sends the user to the appropriate actions
function track {
    cmd=$1
    label=$2
    case "$1" in
	"") echo "To use track provide some command. Use 'track start/stop/status/log'";;
	start) .start $label;;
	stop) .stop;;
	status) .status;;
	log) .log;;
	*) echo "ERROR: Unknown command. Use 'track start/stop/status/log'";;
    esac
}

# The start function starts a new task
function .start {
    label=$1
    
    nStart=$(cat $LOGFILE | grep -c START)
    nEnd=$(cat $LOGFILE | grep -c END)

    if [ $nStart -gt $nEnd ]
    then
	lastTask=$(cat $LOGFILE | grep LABEL | tail -1 | cut -d " " -f5)
	echo "ERROR: You already have an active task named ${lastTask}."
    else
	if [ -z "${label}" ]
	then
	    echo "ERROR: You need to name a new task"
	else
	    echo "START $(date)" | tee -a $LOGFILE
	    echo "LABEL This is task $label" | tee -a $LOGFILE
	fi
    fi
}

# The stop function stops and concludes a task
function .stop {
    nStart=$(cat $LOGFILE | grep -c START)
    nEnd=$(cat $LOGFILE | grep -c END)

    if [ $nStart -gt $nEnd ]
    then
	echo "END $(date)" | tee -a $LOGFILE
	echo "" >> $LOGFILE
    else
	echo "ERROR: No tasks are active and cannot stop a task. Start a new task with start [task]."
    fi
    export ACTIVE=""
}

# The status function provides a summary of the status of tasks
function .status {
    nStart=$(cat $LOGFILE | grep -c START)
    nEnd=$(cat $LOGFILE | grep -c END)
    lastTask=$(cat $LOGFILE | grep LABEL | tail -1 | cut -d " " -f5)
    echo "Number of tasks started: ${nStart}."
    echo "Number of tasks ended: ${nEnd}."
    if [ $nStart -gt $nEnd ]
    then
	echo "One active task named $lastTask."
    else
	echo "No Active tasks."
    fi
}

function .log {
    nStart=$(cat $LOGFILE | grep -c START)
    nEnd=$(cat $LOGFILE | grep -c END)
    lastTask=$(cat $LOGFILE | grep LABEL | tail -1 | cut -d " " -f5)

    declare -a startTimes=($(cat $LOGFILE | grep START | cut -d" " -f5))

    if [ "$nStart" -lt "1" ]
    then
	echo "No tasks has been logged."
    elif [ "$nEnd" -lt "1" ]
    then
	echo "The task $lastTask was started but not finished."
    fi
    
    declare -a endTimes=($(cat $LOGFILE | grep END | cut -d" " -f5))
    declare -a tasks=($(cat $LOGFILE | grep LABEL | cut -d" " -f5))
    
    declare -i i
    i=0
    while [ $i -lt ${#endTimes[@]} ]
    do
	endH=$(echo ${endTimes[i]} | cut -d':' -f1)
	endM=$(echo ${endTimes[i]} | cut -d':' -f2)
	endS=$(echo ${endTimes[i]} | cut -d':' -f3)
	startH=$(echo ${startTimes[i]} | cut -d':' -f1)
	startM=$(echo ${startTimes[i]} | cut -d':' -f2)
	startS=$(echo ${startTimes[i]} | cut -d':' -f3)
	diffH=$((endH-startH))
	diffM=$((endM-startM))
	diffS=$((endS-startS))
	if [ "$diffS" -lt "0" ]
	then
	    diffM=$((diffM-1))
	    diffS=$((diffS+60))
	fi
	if [ "$diffM" -lt "0" ]
	then
	    diffH=$((diffH-1))
	    diffM=$((diffM+60))
	fi
	if [ "$diffH" -lt "0" ]
	then
	    diffH=$((diffH+24))
	fi
	echo "Task ${tasks[i]}: ${diffH}:${diffM}:${diffS}"
	((i++))
    done
    
    
    #echo $((endTimes[0]-startTimes[0]))
}

# This portion ensures the LOGFILE exists and tracks it.
dir=~/.local/share
log=.time_logfile
export LOGFILE=$dir/$log
if [ -z $(ls $dir -a | grep $log) ]
then
    echo "Creating logfile at $LOGFILE"
    touch $LOGFILE
fi
