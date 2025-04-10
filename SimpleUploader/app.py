from flask import Flask, request, render_template, redirect, url_for, send_file
import os
import qrcode
import io
import socket
from werkzeug.utils import secure_filename

app = Flask(__name__)
    

def get_accessible_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # doesn't need to be reachable, just used to select interface
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

LOCAL_IP = get_accessible_ip()
UPLOAD_FOLDER = os.path.expanduser("~/Downloads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/qr')
def generate_qr():
    url = f"http://{LOCAL_IP}:5000"
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files' not in request.files:
            return redirect(request.url)
        files = request.files.getlist('files')
        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('upload_file'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    

