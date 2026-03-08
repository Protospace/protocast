# Protocast

Casts computer screens to the TV displays at Protospace.

Currently used to cast the laser computer screens to the LCARS1 display above the Trotec laser.

## Theory

Start and stop Protocast shortcuts on the desktop of each PC run a PowerShell script that sends POST requests to the script running on the desired display.

The shortcut sends ie. `machine=trotec` POST data to `/cast` route to start casting. The script runs a `xtightvncviewer -viewonly -fullscreen [IP]` command via subprocess to VNC into the respective machine. 

A POST to `/stop` runs `killall xtightvncviewer`.


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

Setting up a PC for casting to the display above the Trotec:
- Example case is "xtool" - change to accomodate actual machine name (ex: "108mediapc")
- Assumes the machine is already on the Windows domain


Step 1: Assign the computer a static IP:
- Get the Ethernet MAC address
- Go to pfSense
- Grant the machine a static IP in it's VLAN if not already done so (steps not described here)

Step 2: Install TightVNC server:
- Grab TightVNC server from https://www.tightvnc.com/download.php
- Install, in "Complete" mode
- At the next prompt, check "Run only as a system service, disable user application mode"
- When prompted, uncheck password, check no password *** SUBJECT TO CHANGE, THIS PROCESS IS BEING LOOKED AT FOR IMPROVEMENT**

Step 3: Copy the files:

*At time of writing, ensure to use the "xtool" computer as the source for this step, as it has fixes for improved security in newer PowerShell versions, required in Windows 11, possibly in newer patches in Windows 10 as well) -- these fixes are yet to be applied to other machines (2026-03-08)*

- Copy `C:\windows\psfiles\protocast*` files from another machine to this machine's `C:\windows\psfiles` folder
- Copy the Protocast ON and Protocast OFF files from another machine to this machine's `C:\Users\Public\Desktop\` folder (the "all users" desktop, otherwise it would only appear on *your user's* desktop
- Right click protocast.cmd (shortcut) in `C:\windows\psfiles` and click properties
  - change the name after the space to a unique name (slug) for this machine
- Right click "Protocast ON" (shortcut) in `C:\Users\Public\Desktop\` and repeat the step above with the same name.
- Right click "protocast.ps1" (Powershell script) in `C:\windows\psfiles\` and edit the file
  - in the param section, add a new valid string for the name you chose in previous steps, ex: `[ValidateSet("thunder", "xtool", "trotec", "stop")]` becomes `[ValidateSet("thunder", "xtool", "trotec", "108mediapc", "stop")]`
  - in the switch ($Action) section, copy another PC's section ("{...}") to create the new entry, if machines from multiple areas of the shop exist, choose one to copy from that already casts to the screen that you wish this new computer to cast to
  - in your pasted copy, update the name in the two places (first line of the copied section, and the "machine" = "xyz" line, again, using the same name chosen previously)

Step 4: Ensure auto-stop on logout applies (AD):

If the computer is not in the "Laser Computers OU" in AD, a GPO for a logoff script to run the "Off" command on user logout will need to be created that applies to this machine -- this is not a default on all machines as this script doesn't exist on most machines. Copy from the existing Group Policy applying in the Laser Computers OU, ensuring to scope to only the computer(s) that have protocast set up, and the default "authenticated users" scope item is removed. After doing this step, run a `gpupdate /force` on the target computer and reboot it.

Step 5: Update the display machine's scripts to know new computer:
- Edit `main.py` and add an `elif` case for the machine's name that gets sent by the shortcut
- Duplicate the `def cast_thunder()` function and make it specific to the new machine that was added
- Make sure the IP address matches the one assigned earlier
- Restart Protocast: `$ sudo supervisorctl restart protocast`
