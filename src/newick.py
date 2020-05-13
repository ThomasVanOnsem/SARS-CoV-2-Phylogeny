def construct_json(structure, newick_string, tree=None, placement=False):
    amount_leafs = 0

    if tree is None:
        tree = {"children": {}}
    internal_str = newick_string[structure['begin'] + 1:structure['end']]
    internal_list = internal_str.split(',')
    for leaf_unf in internal_list:
        tree_element = {}
        if '(' in leaf_unf or ')' in leaf_unf:
            # not a leaf
            continue
        element_name, element_length = leaf_unf.split(':')
        if placement:
            element_length, node_index = element_length.split('{')
            # Remove last curly bracket from index
            node_index = node_index[:-1]
            tree_element["index"] = node_index

        tree_element["name"] = element_name
        tree_element["length"] = element_length
        tree_element["children"] = {}
        tree_element["leafCount"] = 1
        tree["children"][element_name] = tree_element
        #the leaf is a child of this node
        amount_leafs += 1
    for child in structure["children"]:
        tree_element = {}
        element_specification = newick_string[child["end"]+1:]
        element_name_length_str = element_specification.split(':')
        element_name = element_name_length_str[0]
        #in the middle it is comma seperated only at the end point comma
        end_length = element_name_length_str[1].find(',')
        if end_length == -1: end_length = element_name_length_str[1].find(')')
        if end_length == -1: end_length = element_name_length_str[1].find(';')
        element_length = element_name_length_str[1][:end_length]

        if placement:
            # TODO element length is incorrect so following code will make it crash
            pass
            # element_length, node_index = element_length.split('{')
            # # Remove last curly bracket from index
            # node_index = node_index[:-1]
            # tree_element["index"] = node_index

        #for inner nodes we don't insert names
        tree_element["length"] = element_length
        tree_element["children"] = {}

        tree_element, new_amount_leafs = construct_json(child, newick_string, tree_element, placement=placement)
        amount_leafs += new_amount_leafs
        tree_element["leafCount"] = new_amount_leafs

        tree["children"][element_name] = tree_element
    return tree, amount_leafs

#helperfunc to convert neweck to json (as this is more usefull for handling in jquery)
def convert_newick_json(newick_file, placement=False):
    content = open(newick_file, "r")
    if content:
        newick_string = content.readline()


        current_node = None
        #we keep where the last bracket was opened to find the inner text of 'leaves'
        last_open = -1
        #we first combine all positions of an opening parentheses with the position of the closing one
        for iter in range(0, len(newick_string)):
            if newick_string[iter] == '(':
                last_open = iter
                node = {
                    'parent': current_node,
                    'begin': iter,
                    'end': None,
                    'children': []
                }
                if current_node is not None:
                    current_node['children'].append(node)
                current_node=node

            if newick_string[iter] == ')':
                current_node['end'] = iter
                if current_node['parent'] is not None:
                    current_node = current_node['parent']

        if current_node is None:
            return None

        tree_json, amount_leafs = construct_json(current_node, newick_string, placement=placement)
        #-2 because 1 for the top node and one because the root also adds one
        tree_json['leafCount'] = amount_leafs
        return tree_json
