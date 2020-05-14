import json
import os
from subprocess import check_call
from newick import convert_newick_json
from phylo.align import alignOne
from tools import getDataLocation, makeTempDirectory


def makeReferencePackage(treeFile, alignmentFile, logFile, output):
    check_call(['rm', '-r', output])
    cmd = f"""
            ../taxit_venv/bin/taxit create
                -l 16s_rRNA -P {output}
                --aln-fasta {alignmentFile}
                --tree-stats {logFile} 
                --tree-file {treeFile}
    """
    check_call(cmd.split())


def makePlacement(fastaFile: str, proteinName: str, ID: str):
    proteinName = proteinName.replace(' ', '_')
    makeTempDirectory()

    # Align the sequence against the reference alignment
    referenceAlignmentFile = getDataLocation(f'alignments/{proteinName}.fasta')
    mergedAlignmentFile = getDataLocation(f'tmp/merged_{ID}.fasta')
    alignOne(fastaFile, referenceAlignmentFile, mergedAlignmentFile)

    # Make placement using pplacer
    packageFile = getDataLocation(f'reference_packages/{proteinName}.refpkg')
    placementFile = getDataLocation(f'tmp/{ID.__hash__()}.jplace')
    # To prevent crash in pplacer
    os.environ['LANG'] = '/usr/lib/locale/en_US'
    cmd = f'../lib/pplacer -o {placementFile} -c {packageFile} {mergedAlignmentFile}'
    check_call(cmd, shell=True)

    with open(placementFile) as file:
        placement = json.load(file)

    # Remove temp files
    os.remove(mergedAlignmentFile)
    os.remove(placementFile)

    return placement


def placementToJsonVisualisation(placementJson, ID: str):
    indices = {
        'like_weight_ratio': None,
        'edge_num': None,
        'distal_length': None,
        'pendant_length': None
    }

    for index, field in enumerate(placementJson['fields']):
        indices[field] = index

    placements = dict()
    for placement in placementJson['placements']:
        for p in placement['p']:
            edge = str(p[indices['edge_num']])
            placements[edge] = {
                'likelihood_percentage': p[indices['like_weight_ratio']],
                'distal_length': p[indices['distal_length']],
                'pendant_length': p[indices['pendant_length']]
            }

    placementTree = getDataLocation(f'tmp/{ID.__hash__()}.newick')
    with open(placementTree, 'w') as file:
        json.dump(placementJson['tree'], file)

    newick_json = convert_newick_json(placementTree, placement=True)

    addPlacements(newick_json, placements)

    # TODO remove
    with open('plac.jplace', 'w') as file:
        json.dump(placementJson, file)
    with open('newick.json', 'w') as file:
        json.dump(newick_json, file)

    return newick_json


def addPlacements(tree: dict, placements: dict):
    """ Traverse tree and add placements """
    for key in tree['children']:
        elem = tree['children'][key]
        if elem['index'] in placements:
            elem['placement'] = True
            elem['likelihood'] = placements[elem['index']]['likelihood_percentage']

        # Recursive call
        addPlacements(elem, placements)
