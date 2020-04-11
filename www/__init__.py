from flask import Flask, render_template, request, redirect, jsonify, url_for
import os
from werkzeug.utils import secure_filename
#from src.phylo_proteins.main import generateProteinPhylo


ALLOWED_EXTENSIONS = {'txt', 'fasta'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '../data/'
app.config['IMAGE_FOLDER'] = '../results/'


@app.route('/')
def homepage(image_location=None):
    if image_location:
        return render_template('home.html', phylo_image=image_location)
    else:
        return render_template('home.html')


@app.route("/features")
def features():
    return render_template('features.html')


@app.route('/get-stored-sequences', methods=['GET'])
def getStoredSequences():
    return jsonify({})  # TODO what?


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
        # generateProteinPhylo('../data/filename', filename)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # return_filename = os.path.join(app.config['IMAGE_FOLDER'], filename + '.png')
        return_filename = '../static/spike-phylo.png'
        return homepage(return_filename)
    if sequence:
        # generateProteinPhylo(sequence)
        return redirect(url_for('homepage'))
    return jsonify({'success': False, 'file': filename}), 400, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run()
