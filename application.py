from flask import Flask, jsonify, request, render_template, redirect
import boto3
import uuid
import os

application = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
table = dynamodb.Table('short-urls')

@application.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "online"} ), 200

@application.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@application.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('long_url')

    if not long_url:
        return jsonify({"error": "URL Needed"}), 400
    
    if not long_url.startswith(('http://', 'https://')):
        long_url = 'https://' + long_url

    short_id = str(uuid.uuid4())[:6]

    try:
        table.put_item(
            Item={
                'short_id': short_id,
                'long_url': long_url
            }
        )
        
        base_url = request.host_url
        short_url = f"{base_url}{short_id}"

        return jsonify({
            "short_id": short_id,
            "short_url": short_url,
            "original_url": long_url
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@application.route('/<short_id>', methods=['GET'])
def redirect_to_url(short_id):
    try:
        response = table.get_item(Key={'short_id': short_id})
        item = response.get('Item')

        if item:
            return redirect(item['long_url'])
        else:
            return "URL tidak ditemukan atau sudah kadaluwarsa.", 404
            
    except Exception as e:
        return jsonify({"error": "Terjadi kesalahan pada server"}), 500
    
if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=5000)  