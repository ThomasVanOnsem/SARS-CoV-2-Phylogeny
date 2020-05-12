from flask import Flask, render_template, request, redirect, jsonify, url_for
import os
import traceback
from datetime import datetime
from werkzeug.utils import secure_filename
from newick import convert_newick_json
from tools import getDataLocation
from src.phylo.placement import makePlacement
from src.phylo.fasta import parseFasta

ALLOWED_EXTENSIONS = {'txt', 'fasta'}

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


@app.route('/placement', methods=['POST'])
def makePlacement():
    # TODO unfinished
    data = request.get_json()
    seq = data['seq']
    placementJson = makePlacement('surface glycoprotein', seq.strip(), 'my_protein')
    newickJson = placementToJsonVisualisation(placementJson)
    return jsonify(newickJson)


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


def makeFastaFile(proteinName: str, origin: str, sequence: str, seq_id: str):
    filename = f'addition{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}'
    f = open(getDataLocation(f'tmp/') + filename, 'x')
    f.write(f'{seq_id}|{proteinName}|{origin}\n{sequence}')
    f.close()
    return filename


@app.route('/submit-data', methods=["POST"])
def submit_data():
    data = request.form
    if data['nuc-id'] or data['amino-id']:
        if data['nuc-id']:
            file = makeFastaFile(proteinName=data['proteinChoice'], origin=data['nuc-origin'], sequence=data['nuc-sequence'],
                                 seq_id=data['nuc-id'])
        else:
            file = makeFastaFile(proteinName=data['proteinChoice'], origin=data['amino-origin'], sequence=data['amino-sequence'],
                                 seq_id=data['amino-id'])
        try:
            makePlacement(getDataLocation(f'tmp/{file}'))
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 200, {'ContentType': 'application/json'}
        os.remove(getDataLocation(f'tmp/{file}'))
        return jsonify({'success': True}), 200, {'ContentType': 'application/json'}

    files = request.files
    if files['nuc-file'].filename:
        f = files['nuc-file']
    else:
        f = files['amino-file']
    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)
        f.save(getDataLocation(f'tmp/'), filename)
        try:
            makePlacement(getDataLocation(f'tmp/{filename}.fasta'))
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 200, {'ContentType': 'application/json'}
        os.remove(getDataLocation(f'tmp/{filename}.fasta'))
    return jsonify({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    app.run()
