# Protocast

Casts computer screens to the TV displays at Protospace.

Currently used to cast the laser computer screens to the LCARS1 display above the Trotec laser.

## Setup

### Windows PC Scripts

#### On any Domain Controller
Create the following files in the \\ps\netlogon\protocast\ directory"
* protocast.ps1
* protocast ON.lnk
* protocast OFF.lnk

There are 2 additional files are provided for additional reference but are not required.
* protocast.cmd 
This files provides a command line that is actually in the shortcut. 
* IPAddress.ps1
This script runs just the ipAddress command and displays the result to the screen. 

The shortcuts can be created manually using the following properties"  \
**Target:** `powershell.exe -ExecutionPolicy Bypass -File \\ps\netlogon\protocast\protocast.ps1 start`  
or  
**Target:** `powershell.exe -ExecutionPolicy Bypass -File \\ps\netlogon\protocast\protocast.ps1 stop`  

**Run:** Minimized

