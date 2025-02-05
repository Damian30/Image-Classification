from flask import Flask, render_template, jsonify, redirect, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
import training
import numpy as np
from keras.preprocessing import image

app = Flask(__name__, static_url_path='/static')

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

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
        if not allowed_file(file.filename):
            print('Not an allowed extension of file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #print("I am inside the main loop")
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            with training.graph.as_default():

                test_image = image.load_img('uploads/' + filename, target_size = (64, 64))
                test_image = image.img_to_array(test_image)
                test_image = np.expand_dims(test_image, axis = 0)
                result = training.classifier.predict(test_image)

                S = [['bird', result[0][0]], ['cat', result[0][1]], ['dog', result[0][2]]]

                answer = sorted(S, key = lambda x : x[1], reverse = True)[0][0]

                return render_template('answer.html', answer=answer, filename=filename)
                
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__ == "__main__":
    app.run(debug=True)