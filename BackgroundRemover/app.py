from flask import Flask, request, send_file, render_template
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def remove_background():
    try:
        if 'image' not in request.files:
            return {'error': 'No image provided'}, 400
        
        file = request.files['image']
        input_image = file.read()
        
        output_image = remove(input_image)
        
        output_io = io.BytesIO(output_image)
        output_io.seek(0)
        
        return send_file(output_io, mimetype='image/png', as_attachment=True, download_name='output.png')
    
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
