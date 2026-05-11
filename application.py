from flask import Flask, jsonify

application = Flask(__name__)

@application.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "online"}), 200

@application.route('/', methods=['GET'])
def index():
    return jsonify({"message": "URL Shortener API is running"}), 200

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=5000)  