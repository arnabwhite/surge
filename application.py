from flask import Flask, jsonify, request, render_template
import boto3
import uuid
import os

application = Flask(__name__)

@application.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "online"}), 200

@application.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@application.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('long_url')

    if not long_url:
        return jsonify({"error": "URL Needed"}), 400

    short_id = str(uuid.uuid4())[:6]

    try:
        table.put_item(
            Item={
                'short_id': short_id,
                'long_url': long_url
            }
        )
        
        short_url = f"http://surge-app-env.eba-mvgjnfm4.ap-southeast-1.elasticbeanstalk.com/{short_id}"
        return jsonify({
            "short_id": short_id,
            "short_url": short_url,
            "original_url": long_url
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=5000)  