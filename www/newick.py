def construct_json(structure, newick_string, tree=None):
    depth = 0

    if tree is None:
        tree = {"children": {}}
    for child in structure["children"]:
        tree_element = {}
        element_specification = newick_string[child["end"] + 1:]
        name_length = element_specification.split(':')
        element_name = name_length[0]
        end_length = name_length[1].find(';')
        if end_length == len(name_length[1]): end_length = name_length[1].find(')')
        element_length = name_length[1][:7]

        tree_element["length"] = element_length
        tree_element["children"] = {}

        tree_element, newDepth = construct_json(child, newick_string, tree_element)
        if depth < newDepth:
            depth = newDepth

        tree["children"][element_name] = tree_element

    return tree, depth+1


#helperfunc to convert neweck to json (as this is more usefull for handling in jquery)
def convert_newick_json(newick):
    content = open(newick, "r")
    if content:
        newick_string = content.readline()


        start_node = {'children': []}
        current_node = start_node
        #we first combine all positions of an opening parentheses with the position of the closing one
        for iter in range(0, len(newick_string)):
            if newick_string[iter] == '(':
                node = {
                    'parent': current_node,
                    'begin': iter,
                    'end': None,
                    'children': []
                }
                current_node['children'].append(node)
                current_node=node

            if newick_string[iter] == ')':

                current_node['end'] = iter
                current_node = current_node['parent']


        tree_json, depth = construct_json(start_node, newick_string)
        #-2 because 1 for the top node and one because the root also adds one
        tree_json['depth'] = depth-2
        return tree_json
