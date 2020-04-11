from flask import Flask, render_template, request, redirect, jsonify
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '../data/'
ALLOWED_EXTENSIONS = {'txt', 'fasta'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route("/features")
def features():
    return render_template('features.html')


@app.route('/get-stored-sequences', methods=['GET'])
def getStoredSequences():
    return jsonify({})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/submit-data', methods=['POST'])
def submit_data():
    """Generate for a file."""
    f = request.files['file']
    sequence = request.form['sequence-text']
    filename = ""
    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("File saved.")
        #generateProteinPhylo('../data/filename')
        return jsonify({'success': True, 'file': filename}), 200, {'ContentType': 'application/json'}
    if sequence:
        #generateProteinPhylo(sequence)
        return jsonify({'success': True, 'file': filename}), 200, {'ContentType': 'application/json'}
    return jsonify({'success': False, 'file': filename}), 400, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run()
