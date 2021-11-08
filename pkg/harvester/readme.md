# Harvester

A script to collect small files in one place and compress them into an archive for backup purposes.

## Options file

This utility requires configuration in the form of an `options.json` file.

* files
    * Array of paths of files and directories to sync
* path_sync
    * Path to directory to sync the files to
* path_sync_log
    * Path to logfile of synced files
* path_arch
    * Path to directory to move the compressed archive to
* args_sync
    * Array of additional arguments to rsync
* cmd_arch
    * Command to run for archiving the synced files (7z recommended)