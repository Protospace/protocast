# Protocast

Casts computer screens to the TV displays at Protospace.

Currently used to cast the laser computer screens to the LCARS1 display above the Trotec laser.

## Theory

Start and stop Protocast shortcuts on the desktop of each PC run a PowerShell script that sends POST requests to the script running on the desired display.

The shortcut sends data ie. `ip_address=172.17.17.214` POST data to `/cast` route to start casting. The script runs a `xtightvncviewer -viewonly -fullscreen [IP]` command via subprocess to VNC into the respective machine. 

A POST to `/stop` first checks to see if there is a current cast session in progress, checks to see if the calling machine is the last requesting ip_address, and if it is then runs `killall xtightvncviewer`.

This is to prevent a PC from killing a cast that is in progress from another PC.


## Setup

### TV Display Script

Log into display computer, clone script:

```
$ ssh protospace@10.139.88.128
$ sudo apt install git python3 python3-pip python3-virtualenv supervisor xtightvncviewer
$ git clone https://github.com/Protospace/protocast.git
$ cd protocast/
$ virtualenv -p python3 env
$ . env/bin/activate
(env) $ pip install -r requirements.txt
(env) $ python main.py
```

To deploy, edit `/etc/supervisor/conf.d/protocast.conf`:

```
[program:protocast]
user=protospace
directory=/home/protospace/protocast
command=/home/protospace/protocast/env/bin/python -u main.py
stopsignal=INT
stopasgroup=true
killasgroup=true
autostart=true
autorestart=true
stderr_logfile=/var/log/protocast.log
stderr_logfile_maxbytes=10MB
stdout_logfile=/var/log/protocast.log
stdout_logfile_maxbytes=10MB
```

Load config:

```
$ sudo supervisorctl reread; sudo supervisorctl update
```


### Windows Computers

Setting up a PC for casting to the display on the wall above the Trotec:
- Assumes the machine is already on the Windows domain
- The IP Address of the Windows PC is allowed in the Display computer's configuration

There in no customization required to the files for a new PC.  (This was updated on 03/10/2026). It runs the scripts directly from the Domain's NETLOGON directory.

The only files that need to be copied at the Desktop shortcuts to be placed on the "All Users" Desktop. 

Step 1: Assign the computer a static IP:
- Get the Ethernet MAC address
- Go to pfSense
- Grant the machine a reserved static IP in it's VLAN if not already done so (steps not described here)

Step 2: Install TightVNC server:
- Grab TightVNC server from https://www.tightvnc.com/download.php
- Install, in "Complete" mode
- At the next prompt, check "Run only as a system service, disable user application mode"
- When prompted, uncheck password, check no password *** SUBJECT TO CHANGE, THIS PROCESS IS BEING LOOKED AT FOR IMPROVEMENT**

Step 3: Copy the files:

- Copy `\\ps\netlogon\protocat\protocast*.lnk` files from the Domain to this machine's `C:\Users\Public\Desktop\` folder (the "all users" desktop, otherwise it would only appear on *your user's* desktop

Step 4: Ensure auto-stop on logout applies (AD):

If the computer is not in the "Laser Computers OU" in AD, a GPO for a logoff script to run the "Off" command on user logout will need to be created that applies to this machine -- this is not a default on all machines as this script doesn't exist on most machines. Copy from the existing Group Policy applying in the Laser Computers OU, ensuring to scope to only the computer(s) that have protocast set up, and the default "authenticated users" scope item is removed. After doing this step, run a `gpupdate /force` on the target computer and reboot it.
