import os
from tree_sitter import Language, Parser
import sys

# Define the path to the tree-sitter languages and the language you want to use
LANGUAGE_NAME = 'c'
LANGUAGE_SO = './tree-sitter-c.so'

def strip_c_style_comment_delimiters(comment: str) -> str:
    comment_lines = comment.split('\n')
    cleaned_lines = []
    for l in comment_lines:
        l = l.strip()
        if l.endswith('*/'):
            l = l[:-2]
        if l.startswith('*'):
            l = l[1:]
        elif l.startswith('/**'):
            l = l[3:]
        elif l.startswith('//'):
            l = l[2:]
        cleaned_lines.append(l.strip())
    return '\n'.join(cleaned_lines)

def get_docstring_summary(docstring: str) -> str:
    """Get the first lines of the documentation comment up to the empty lines."""
    if '\n\n' in docstring:
        return docstring.split('\n\n')[0]
    elif '@' in docstring:
        return docstring[:docstring.find('@')]  # This usually is the start of a JavaDoc-style @param comment.        
    return docstring

# Load the language library
if not os.path.exists(LANGUAGE_SO):
    Language.build_library(
        LANGUAGE_SO,
        [f'tree-sitter-{LANGUAGE_NAME}']
    )

C_LANGUAGE = Language(LANGUAGE_SO, LANGUAGE_NAME)

# Initialize the parser
parser = Parser()
parser.set_language(C_LANGUAGE)

# Read C code from a file
fname = sys.argv[1]
with open(f"{fname}", 'rb') as file:
    code = file.read()

# Parse the code
tree = parser.parse(code)

# Function to tokenize a string (split into words)
def tokenize(text):
    return text.split()


# Function to clean comment text
def clean_comment_text(comment):
    lines = comment.split('\n')
    cleaned_lines = []
    for line in lines:
        # Remove comment syntax (/*, */, //) and leading asterisks
        line = line.strip().strip('/*').strip('*/').strip('*').strip('//').strip()
        if line:  # Avoid adding empty lines
            cleaned_lines.append(line)
    return ' '.join(cleaned_lines)

# Function to extract information from function nodes
def extract_function_info(node, source_code, last_comment):
    function_name = ''
    parameters = []
    comment = clean_comment_text(last_comment) if last_comment else None

    # Extract the entire function text
    function_text = source_code[node.start_byte:node.end_byte].decode('utf8')
    function_text = ' '.join(tokenize(function_text))
    tokenized_function = tokenize(function_text)
    tokenized_comment = tokenize(comment) if comment else []

    # Get the start line number of the function
    start_line_number = node.start_point[0] + 1  # Tree-sitter line numbers are 0-indexed
    
    # Traverse the tree starting from the function node
    cursor = node.walk()
    visited = set()
    
    while True:
        # Get the current node
        n = cursor.node
        
        if n.id in visited:
            # Go to the next sibling if the current node is already visited
            if not cursor.goto_next_sibling():
                if not cursor.goto_parent():
                    break
        else:
            visited.add(n.id)
            
            # Check the type of the current node
            if n.type == 'function_definition':
                function_name = n.child_by_field_name('declarator').child_by_field_name('declarator').text.decode('utf8')
            elif n.type == 'parameter_list':
                parameters = [param.text.decode('utf8') for param in n.children if param.type == 'parameter_declaration']
            
            # Visit children
            if not cursor.goto_first_child():
                if not cursor.goto_next_sibling():
                    if not cursor.goto_parent():
                        break    
    return function_name, parameters, comment, function_text, tokenized_function, tokenized_comment, start_line_number

# Extract information from each function and associate comments with functions
root_node = tree.root_node
last_comment = None

for node in root_node.children:
    if node.type == 'comment':
        last_comment = code[node.start_byte:node.end_byte].decode('utf8')
    elif node.type == 'function_definition':
        function_name, parameters, function_comment, function_text, tokenized_function, tokenized_comment, line_number = extract_function_info(node, code, last_comment)
        print(f'Function Name: {function_name}')
        print(f'Line: {line_number}')
        print(f'Parameters: {parameters}')
        if function_comment:
            print(f'Comments: {function_comment}')
            print(f'Tokenized Comments: {tokenized_comment}')
        else:
            print('Comments: ')
        print(f'Function Text: {function_text}')
        print(f'Tokenized Function: {tokenized_function}')        
        print('---')
        last_comment = None  # Reset last_comment after associating it with a function
