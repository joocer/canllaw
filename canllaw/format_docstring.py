import re

known_headers = (
    'parameters',
    'arguments',
    'args',
    'returns',
    'yields',
    'example',
    'examples',
    'note',
    'warning',
    'raises'
)

def measure_indent(line):
    for indent, char in enumerate(line):
        if char not in [' ']:
            return indent
    return -1

def strip_non_alpha_num(raw):
    pattern = re.compile(r"[\W_]+")
    return pattern.sub("", raw)

def create_md_content(doc_string):

    last_indent = -1
    cache = '## CLASS NAME'
    for line in doc_string.splitlines():

        indent = measure_indent(line)
        line = line.strip()
        
        header = [h for h in known_headers if strip_non_alpha_num(line.lower()) == h]
        if len(header) == 1:
            cache += '\n### ' + header.pop().title() + '\n'
            last_indent = 100
            continue
    
        if last_indent == indent:
            # if its the same indent, its a line continuation
            cache += line
        else:
            if last_indent > indent:
                # this is an inner_header
                parts = line.split(':')
                for index, part in enumerate(parts):
                    if index == 0:
                        cache += '\n- **' + part + '**  '
                    else:
                        cache += ' - ' + part + '  '
            else:
                # this is the body of the inner_header
                cache += '\n' + line

        last_indent = indent

    return cache

doc = open('doc.txt', mode='r').read()
md = create_md_content(doc)

open('doc.md', mode='w').write(md)