# veeam-foders.sync

Program that synchronizes two folders: source and replica. The program should maintain a full, identical copy of source folder at replica folder.

## Requirements

 * Synchronization must be one-way: after the synchronization content of the replica folder should be modified to exactly match content of the source folder;

 * Synchronization should be performed periodically;

 * File creation/copying/removal operations should be logged to a file and to the console output;

 * Folder paths, synchronization interval and log file path should be provided using the command line arguments;

 * It is undesirable to use third-party libraries that implement folder synchronization;

 * It is allowed (and recommended) to use external libraries implementing other well-known algorithms. For example, there is no point in implementing yet another function that calculates MD5 if you need it for the task – it is perfectly acceptable to use a third-party (or built-in) library;

## Usage

```batch
python3 [path/to]/foders_sync.py  [-h]  SOURCE_FOLDER_PATH  REPLICA_FOLDER_PATH  SYNC_FREQ  LOG_FILE_PATH
```

### positional arguments:
|argument|description|
|-|-|
|SOURCE_FOLDER_PATH|Path to the source folder|
|REPLICA_FOLDER_PATH|Path to the replica folder|
|SYNC_FREQ|Synchronization frequency in seconds|
|LOG_FILE_PATH|Path to the log file|

### optional arguments:
|argument|description|
|-|-|
|-h, --help|show this help message and exit|

### example
```batch
python3 ~/veeam-foders.sync/foders_sync.py ~/origin_dir ~/target_dir 60 ~/foders_sync.log
```
