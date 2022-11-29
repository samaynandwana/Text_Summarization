from flask import Flask, render_template, url_for, request, redirect, flash, send_from_directory
from summarize import summarize
import os
from werkzeug.utils import secure_filename
from collections import Counter
from nltk.corpus import stopwords


app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt'}
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
stopWords = ['a', 'an', 'the', 'and', 'it', 'for', 'or', 'but', 'in', 'my', 'your', 'our', 'their', 'of', 'to']

def remove_stopwords(file_text):
        return [word for word in file_text.split() if word.lower() not in stopWords]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def most_common_words(split_file):
    counter = Counter(split_file)
    most_occur = counter.most_common(4)
    return most_occur

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
                without_stopwords = remove_stopwords(lines)
                most_common = most_common_words(without_stopwords)
                return render_template('summary.html', summary=summary, most_common_words=most_common)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)