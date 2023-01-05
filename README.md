# Presentiment App
TODO: Add description

## Requirements
* Python 3.9
* Windows 10 or 11
  
## Set Up
1. Install pipenv if not installed: `python3 -m pip install --user pipenv`
2. Run `PIPENV_VENV_IN_PROJECT=1 pipenv sync` to install dependencies
3. If your PsyREG.dll file is in a different folder, please set the environment variable PSYREG. You can either set the environment variable manually or add it to your .env file. This is only needed if the file is in a different folder than this project or if the file is named differently.
   1.  `export PSYREG = <FULL PATH TO FILE>`  This needs to be done every time you open the project in a new terminal
   2.  `cp src/env.example src/.env` Open the .env file created by the command and add the full path to the file. This needs to be done only once as it will get saved in your computer.

## Running the code
If you use `python <command>`in your command line, use the following command to run the program:
```
pipenv run presentiment
```

If you use `python3 <command>`in your command line, use the following command to run the program:
```
pipenv run presentiment3
```

## Configuration
* Interval between 0 and 99 seconds
* Max no. of trials = 99
* To easily export to CSV/Spreadsheet, add the ".csv" extension
* For Neulog, you need to open Neulog API

# Development
We use VSCode for development and the extension Better Comments to make our files friendly for developers, here is a list of the possible tags to be used with this extension:
* #$ Indicates a title
* #& Indicates a subtitle 
* #! Indicates a warning message
* #* Indicates a demo
* #? Indicates an unknown or an explanation
* #TODO Indicates a missing but planned feature
* #x Indicates something that was removed


