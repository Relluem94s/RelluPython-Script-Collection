from flask import Flask, request, render_template_string, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = os.path.expanduser("~/Downloads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>Datei Upload</title>
  </head>
  <body>
    <div class="container mt-5">
      <div class="card shadow rounded-4 p-4">
        <h2 class="mb-4 text-center">Dateien hochladen</h2>
        <form method="post" enctype="multipart/form-data">
          <div class="mb-3">
            <input class="form-control" type="file" name="files" multiple>
          </div>
          <button type="submit" class="btn btn-primary w-100">Hochladen</button>
        </form>
      </div>
    </div>
  </body>
</html>
'''

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
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

