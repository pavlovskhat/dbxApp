# Demo Sync App using Dropbox API 2.0
###### Application allows user to sync a local folder with dropbox.


Setup Instructions: 
Create a demo dropbox app here: https://www.dropbox.com/developers/apps
On permissions tab allow following:
  - file metadata read and write
  - file content read and write
  - file requests read and write
Submit the changes and generate a Token on the settings tab
Copy paste the Token into the script next to variable labeled "TOKEN" above main 
Add the local path for your folder in the script above main function

## Application menu functions
1. Backup local files
2. View local files
3. View dropbox files
4. Exit application

NOTE: application will attempt to establish a connection with dropbox and find
local directory, if an error occurs in either process application will close
before moving to menu options.

## Backup Local Files
Application will use connection to read files in dropbox after which it will
walk through all folders, sub folders and files in local directory.
If files with duplicate names are found user will be asked for overwrite
permission. Unique files will be uploaded without prompt.


## View Local Files
User will be able to view names of local files.

## View Dropbox Files
User will be able to view dropbox files.

## Exit
Application will end.

