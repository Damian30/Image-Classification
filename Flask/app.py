from flask import Flask, render_template, jsonify, redirect, request
import os

app = Flask(__name__, static_url_path='/static')

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg', '.gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file = request.files['image']
            f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(f) 
    return render_template('index.html')

    # add your custom code to check that the uploaded file is a valid image and what type of pet is in store

if __name__ == "__main__":
    app.run(debug=True)