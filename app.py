from flask import Flask, render_template, url_for, request, redirect, flash
from summarize import summarize
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)