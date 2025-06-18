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

def main():
    app.run(debug=DEBUG, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

if __name__ == '__main__':
    main()
