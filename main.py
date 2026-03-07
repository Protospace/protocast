import os, logging, subprocess, threading
DEBUG = os.environ.get('DEBUG')
logging.basicConfig(
        format='[%(asctime)s] %(levelname)s %(module)s/%(funcName)s - %(message)s',
        level=logging.DEBUG if DEBUG else logging.INFO)

from flask import Flask, request

# Constants
AUTO_STOP_TIMEOUT_SECONDS = 3600  # 1 hour

app = Flask(__name__)
auto_stop_timer = None # Timer for automatic VNC stop

@app.route('/cast', methods=['POST'])
def cast_spell():
    machine = request.form.get('machine')
    logging.info(f"Received POST request on /cast. Requested machine: {machine}")

    global auto_stop_timer

    if machine == "trotec":
        logging.info("Casting to Trotec.")
        kill_vnc()  # Kill any existing VNC session first
        cast_trotec()
        # Restart auto-stop timer
        if auto_stop_timer is not None and auto_stop_timer.is_alive():
            auto_stop_timer.cancel()
            logging.info("Cancelled previous auto-stop timer.")
        auto_stop_timer = threading.Timer(AUTO_STOP_TIMEOUT_SECONDS, _auto_stop_vnc)
        auto_stop_timer.start()
        logging.info(f"Scheduled auto-stop for VNC in {AUTO_STOP_TIMEOUT_SECONDS} seconds.")
        return f"Successfully cast to Trotec.", 200
    elif machine == "thunder":
        logging.info("Casting to Thunder.")
        kill_vnc()  # Kill any existing VNC session first
        cast_thunder()
        # Restart auto-stop timer
        if auto_stop_timer is not None and auto_stop_timer.is_alive():
            auto_stop_timer.cancel()
            logging.info("Cancelled previous auto-stop timer.")
        auto_stop_timer = threading.Timer(AUTO_STOP_TIMEOUT_SECONDS, _auto_stop_vnc)
        auto_stop_timer.start()
        logging.info(f"Scheduled auto-stop for VNC in {AUTO_STOP_TIMEOUT_SECONDS} seconds.")
        return f"Successfully cast to Thunder.", 200
    elif machine == "xtool":
        logging.info("Casting to XTool.")
        kill_vnc()  # Kill any existing VNC session first
        cast_xtool()
        # Restart auto-stop timer
        if auto_stop_timer is not None and auto_stop_timer.is_alive():
            auto_stop_timer.cancel()
            logging.info("Cancelled previous auto-stop timer.")
        auto_stop_timer = threading.Timer(AUTO_STOP_TIMEOUT_SECONDS, _auto_stop_vnc)
        auto_stop_timer.start()
        logging.info(f"Scheduled auto-stop for VNC in {AUTO_STOP_TIMEOUT_SECONDS} seconds.")
        return f"Successfully cast to XTool.", 200
    else:
        logging.warning(f"Invalid or missing machine parameter: {machine}")
        return f"Invalid or missing 'machine' parameter. Use 'trotec' or 'thunder'.", 400

@app.route('/stop', methods=['POST'])
def stop_cast():
    global auto_stop_timer
    logging.info("Received POST request on /stop.")

    if auto_stop_timer is not None and auto_stop_timer.is_alive():
        auto_stop_timer.cancel()
        auto_stop_timer = None
        logging.info("Manual stop: auto-stop timer cancelled.")
    
    kill_vnc()
    return "Attempted to stop VNC viewers.", 200

def _auto_stop_vnc():
    """Called by the timer to automatically stop VNC."""
    global auto_stop_timer
    logging.info("Auto-stopping VNC viewers due to inactivity timer.")
    kill_vnc()
    auto_stop_timer = None # Clear the timer reference

def cast_trotec():
    """Executes the xtightvncviewer command."""
    command = "DISPLAY=:1 xtightvncviewer -viewonly -fullscreen 172.17.17.214"
    try:
        logging.info(f"Launching command: {command}")
        # Use Popen to run the command in the background (non-blocking)
        subprocess.Popen(command, shell=True)
        logging.info(f"Command '{command}' launched successfully.")
    except FileNotFoundError:
        # This error is more likely if the shell itself (e.g., /bin/sh) is not found,
        # or if 'xtightvncviewer' is not in PATH and the shell fails to find it.
        logging.error(f"Failed to launch VNC for Trotec: Shell or VNC command might not be found. Ensure xtightvncviewer is in PATH and shell is available.")
    except Exception as e: # Catch other potential errors during Popen
        logging.error(f"An error occurred while launching VNC for Trotec with Popen: {e}")

def cast_thunder():
    """Executes the xtightvncviewer command for Thunder."""
    command = "DISPLAY=:1 xtightvncviewer -viewonly -fullscreen 172.17.17.215"
    try:
        logging.info(f"Launching command: {command}")
        # Use Popen to run the command in the background (non-blocking)
        subprocess.Popen(command, shell=True)
        logging.info(f"Command '{command}' launched successfully.")
    except FileNotFoundError:
        # This error is more likely if the shell itself (e.g., /bin/sh) is not found,
        # or if 'xtightvncviewer' is not in PATH and the shell fails to find it.
        logging.error(f"Failed to launch VNC for Thunder: Shell or VNC command might not be found. Ensure xtightvncviewer is in PATH and shell is available.")
    except Exception as e: # Catch other potential errors during Popen
        logging.error(f"An error occurred while launching VNC for Thunder with Popen: {e}")

def cast_xtool():
    """Executes the xtightvncviewer command for XTool."""
    command = "DISPLAY=:1 xtightvncviewer -viewonly -fullscreen 172.17.17.221"
    try:
        logging.info(f"Launching command: {command}")
        # Use Popen to run the command in the background (non-blocking)
        subprocess.Popen(command, shell=True)
        logging.info(f"Command '{command}' launched successfully.")
    except FileNotFoundError:
        # This error is more likely if the shell itself (e.g., /bin/sh) is not found,
        # or if 'xtightvncviewer' is not in PATH and the shell fails to find it.
        logging.error(f"Failed to launch VNC for XTool: Shell or VNC command might not be found. Ensure xtightvncviewer is in PATH and shell is available.")
    except Exception as e: # Catch other potential errors during Popen
        logging.error(f"An error occurred while launching VNC for XTool with Popen: {e}")

def kill_vnc():
    """Executes the killall command for xtightvncviewer."""
    command = "killall xtightvncviewer"
    try:
        logging.info(f"Executing command: {command}")
        # We don't use check=True here because killall returns a non-zero exit code
        # if no processes were killed, which is not necessarily an error in this context.
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info("killall command executed successfully. Processes were likely terminated.")
        else:
            # killall returns 1 if no matching processes were found.
            # Other non-zero codes might indicate other errors.
            logging.warning(f"killall command finished. Exit code: {result.returncode}. Stderr: {result.stderr.strip()}")
            if "no process found" in result.stderr.lower():
                 logging.info("No xtightvncviewer processes were found to kill.")

    except FileNotFoundError:
        logging.error(f"Command not found: killall. Please ensure it is installed and in PATH.")
    except Exception as e:
        logging.error(f"An unexpected error occurred while trying to run killall: {e}")

def main():
    app.run(debug=DEBUG, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

if __name__ == '__main__':
    main()
