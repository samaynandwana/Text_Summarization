from flask import Flask, render_template, url_for, request, redirect, flash, send_from_directory
from summarize import summarize
import os
from werkzeug.utils import secure_filename
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.flask_db
todos = db.todos
ALLOWED_EXTENSIONS = {'txt'}
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
                lines = f.read()
                summary = summarize(lines, 0.05)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)