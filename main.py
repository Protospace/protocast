import os, logging
from flask import Flask, request

DEBUG = os.environ.get('DEBUG')
logging.basicConfig(
        format='[%(asctime)s] %(levelname)s %(module)s/%(funcName)s - %(message)s',
        level=logging.DEBUG if DEBUG else logging.INFO)

app = Flask(__name__)

@app.route('/cast', methods=['POST'])
def cast_spell():
    logging.info(f"Received POST request on /cast. Request data: {request.data}")
    return "Cast successful!", 200

def main():
    app.run(debug=DEBUG, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

if __name__ == '__main__':
    main()
