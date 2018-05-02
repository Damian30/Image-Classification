from flask import Flask, render_template, jsonify, redirect, request
import os

app = Flask(__name__, static_url_path='/static')

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f) 
    return render_template('index.html')

    # add your custom code to check that the uploaded file is a valid image and what type of pet is in store

if __name__ == "__main__":
    app.run(debug=True)