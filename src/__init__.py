from flask import Flask, render_template, request, redirect, jsonify, url_for
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from src.newick import convert_newick_json
from src.phylo.phylo import constructTree, constructNewTree
from src.tools import getDataLocation, makeTempDirectory
from src.phylo.placement import makePlacement, placementToJsonVisualisation

ALLOWED_EXTENSIONS = {'fasta'}

app = Flask(__name__)
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = '../data/'
app.config['RESULT_FOLDER'] = os.path.join(THIS_FOLDER, 'static/results/phylo/')
app.config['EXPLANATION_FOLDER'] = os.path.join(THIS_FOLDER, 'static/protein_explanations/')


@app.route('/')
def homepage():
    return render_template('home.html')


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
    info["origin"] = ""  # TODO origin

    return jsonify(info)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def makeFastaFile(proteinName: str, origin: str, sequence: str, seq_id: str):
    makeTempDirectory()
    filename = getDataLocation(f'tmp/{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.fasta')
    # add permission so muscle can read
    os.umask(0)
    with open(os.open(filename, os.O_CREAT | os.O_WRONLY, 0o777), 'w') as fh:
        fh.write(f'>{seq_id} |{proteinName}|{origin}\n{sequence}')
    return filename


@app.route('/submit-data', methods=["POST"])
def submit_data():
    data = request.form
    proteinName = data['proteinChoice']

    # Make a fasta file if a sequence is given
    if data['id']:
        ID = data['id']
        filename = makeFastaFile(proteinName=proteinName, origin=data.get('origin', 'unknown'), sequence=data['sequence'],
                                 seq_id=data['id'])
    # Save file when uploaded
    else:
        f = request.files['file']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            filename = getDataLocation(f'tmp/{filename}')
            f.save(filename)
            ID = filename.__hash__()
        else:
            return jsonify({'success': False, 'error': "File is not a fasta file or no data is specified!"}), 200, {
                'ContentType': 'application/json'}

    try:
        if data['algorithm'] == 'pplacer':
            placementJson = makePlacement(filename, proteinName, ID)
            newickJson = placementToJsonVisualisation(placementJson, ID)
        else:
            newickJson = constructNewTree(filename, proteinName, False)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 200, {'ContentType': 'application/json'}
    finally:
        os.remove(filename)
    return jsonify({'success': True, 'newick': newickJson}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run()
