# Matrix Wave transmitter demo

## Usage
Installing the virtual environment and packages:
```
sudo bash install.sh
```

Run app:
```
sudo bash run.sh
```

## Troubleshooting 
### No module named 'tkinter'
This module should have been installed with pip from `requirements.txt` while running `install.sh`.
But you can steel see error like this. If you see it, please install this module with following command:

For Ubuntu or other distros with apt: `sudo apt-get install python3-tk`

For Fedora or other distros with dnf: `sudo dnf install python3-tkinter`

Source: https://stackoverflow.com/questions/25905540/importerror-no-module-named-tkinter