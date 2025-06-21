from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configuration
API_CONFIG = {
    "host": os.getenv("API_HOST", "api"),
    "port": int(os.getenv("API_PORT", "8001")),
    "api_key": os.getenv("API_KEY", "your-secret-api-key")
}

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            phone_number = request.form.get('phone_number')
            caption = request.form.get('caption', '')
            
            if 'file' not in request.files:
                return jsonify({'error': 'No file selected'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if file and allowed_file(file.filename):
                # Send file to API
                files = {'file': (file.filename, file, file.content_type)}
                data = {
                    'phone_number': phone_number,
                    'caption': caption
                }
                headers = {'X-API-Key': API_CONFIG['api_key']}
                
                api_url = f"http://{API_CONFIG['host']}:{API_CONFIG['port']}/api/media"
                response = requests.post(api_url, files=files, data=data, headers=headers)
                
                if response.status_code == 200:
                    return jsonify({'success': 'Media sent successfully!', 'data': response.json()})
                else:
                    return jsonify({'error': f'API Error: {response.text}'}), 500
            else:
                return jsonify({'error': 'File type not allowed'}), 400
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('upload.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        message = data.get('message')
        
        if not phone_number or not message:
            return jsonify({'error': 'Phone number and message required'}), 400
        
        # Send to API
        headers = {'X-API-Key': API_CONFIG['api_key']}
        api_url = f"http://{API_CONFIG['host']}:{API_CONFIG['port']}/api/messages"
        
        response = requests.post(api_url, json=data, headers=headers)
        
        if response.status_code == 200:
            return jsonify({'success': 'Message sent successfully!', 'data': response.json()})
        else:
            return jsonify({'error': f'API Error: {response.text}'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)