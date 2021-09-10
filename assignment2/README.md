# README.md Assignment2

## Task 2.1

### Prerequisites

The shell-script move.sh is a prerequisite to run the script contained therein.

### Functionality

bash.sh is a small script designed to move files from one directory to another.

### Missing Functionality

Cannot choose to add date to destination directory

### Usage

To transfer files from directory_A to directory_B use the following commands

```bash
./move.sh directory_A directory_B
```

If the destination directory does not exit you will be promted if you want to create the directory.

```bash
./move.sh $HOME/directories/directory_A $HOME/other_directories/directory_B
```

To only move files of type *.type

```bash
./move.sh folderA folderB .type
```

## Task 2.y

### Prerequisites

The shell script needs to be mounted using 'source'.

```bash
source track.sh
```

### Functionality

Track tracks the time spent on tasks like a stopwatch. You can name a new task, stop a running task, check the status to see if a task is running or not and you can list time spent on all finished tasks.

### Missing Functionality

It is currently not possible to see when the current task waS started. It is also not possible to run more than one task at a time.

### Usage

Start by mounting the script:

```bash
source track.sh
```

To start a new task run

```bash
track start [label]
```

To stop the current task run
```bash
track stop
```

To check if a current task is running and the name of this task run
```bash
track status
```

To see the time spent on finished tasks run
```bash
track log
```