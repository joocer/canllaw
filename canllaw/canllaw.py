import ast
from format_docstring import create_md_content


filepath = "test_class.py"

file_contents = ""
with open(filepath) as fd:
    file_contents = fd.read()
module = ast.parse(file_contents)

cache = '# ' + filepath + '\n'

for node in ast.iter_child_nodes(module):

    if isinstance(node, ast.ClassDef):
        #cache += create_md_content(node, title=node.name)
        class_name = node.name
        child_nodes = list(ast.iter_child_nodes(node))

        init = [child_node for child_node in child_nodes if child_node.name == "__init__"]
        if len(init) > 0:
            init = init.pop()
            cache += create_md_content(init, title=node.name)

        for child_node in [child_node for child_node in child_nodes if child_node.name[1] != '_']:
            print(child_node.name)
            if isinstance(child_node, ast.FunctionDef): 
                cache += create_md_content(child_node, title=child_node.name)
        
    if isinstance(node, ast.FunctionDef):
        cache += create_md_content(node, title=node.name)

open('doc.md', mode='w').write(cache)
