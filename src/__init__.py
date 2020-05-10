from flask import Flask, render_template, request, redirect, jsonify, url_for
import os
from werkzeug.utils import secure_filename
from newick import convert_newick_json
from tools import getDataLocation

ALLOWED_EXTENSIONS = {'txt', 'fasta'}

app = Flask(__name__)
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = '../data/'
app.config['RESULT_FOLDER'] = os.path.join(THIS_FOLDER,'static/results/phylo/')
app.config['EXPLANATION_FOLDER'] = os.path.join(THIS_FOLDER, 'static/protein_explanations/')


@app.route('/')
def homepage(image_location=None):
    if image_location:
        return render_template('home.html', phylo_image=image_location)
    else:
        return render_template('home.html')

@app.route("/data/")
def viewData():
    return render_template('results.html')

@app.route("/data/view/<protein>")
def getImage(protein):
    # the link start at the www file
    image = '/static/results/phylo/' + protein + '.png'

    return jsonify({'image': image})

@app.route("/data/newick/<protein>")
def getNewick(protein):
    newick = getDataLocation(f'phylo/{protein}.newick')
    newick_json = convert_newick_json(newick)
    return jsonify(newick_json)

@app.route("/data/info/<protein>")
def getInfoProtein(protein):
    info = {}

    file = open(app.config["EXPLANATION_FOLDER"] + protein + '.txt', 'r')
    if file:
        info["explanation"] = file.readline()
    else:
        info["explanation"] = ""

    return jsonify(info)

@app.route("/data/info/protein/<variant>")
def getInfoVariant(variant):
    info = {}
    info["name"] = variant

    return jsonify(info)


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
