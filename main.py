import os, logging, subprocess
DEBUG = os.environ.get('DEBUG')
logging.basicConfig(
        format='[%(asctime)s] %(levelname)s %(module)s/%(funcName)s - %(message)s',
        level=logging.DEBUG if DEBUG else logging.INFO)

from flask import Flask, request

app = Flask(__name__)

@app.route('/cast', methods=['POST'])
def cast_spell():
    logging.info(f"Received POST request on /cast. Request data: {request.data}")
    return "Cast successful!", 200

def cast_trotec():
    """Executes the xtightvncviewer command."""
    command = "DISPLAY=:1 xtightvncviewer -viewonly -fullscreen 172.17.17.214"
    try:
        logging.info(f"Executing command: {command}")
        subprocess.run(command, shell=True, check=True)
        logging.info("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed with error: {e}")
    except FileNotFoundError:
        logging.error(f"Command not found: xtightvncviewer. Please ensure it is installed and in PATH.")

def cast_thunder():
    """Executes the xtightvncviewer command for Thunder."""
    command = "DISPLAY=:1 xtightvncviewer -viewonly -fullscreen 172.17.17.215"
    try:
        logging.info(f"Executing command: {command}")
        subprocess.run(command, shell=True, check=True)
        logging.info("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed with error: {e}")
    except FileNotFoundError:
        logging.error(f"Command not found: xtightvncviewer. Please ensure it is installed and in PATH.")

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
