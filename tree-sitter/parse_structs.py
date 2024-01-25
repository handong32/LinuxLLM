import os
from tree_sitter import Language, Parser
import sys

# Define the path to the tree-sitter languages and the language you want to use
LANGUAGE_NAME = 'c'
LANGUAGE_SO = './tree-sitter-c.so'

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

# Function to extract information from nodes of interest (struct, typedef, enum)
def extract_info_from_node(node, source_code, last_comment):
    node_type = node.type
    node_text = source_code[node.start_byte:node.end_byte].decode('utf8')
    comment = clean_comment_text(last_comment) if last_comment else None
    tokenized_node = tokenize(node_text)
    tokenized_comment = tokenize(comment) if comment else []
    
    return node_type, node_text, comment, tokenized_node, tokenized_comment

# Traverse the syntax tree and process nodes of interest
root_node = tree.root_node
last_comment = None
for node in root_node.children:
    print(node.type)
    if node.type == 'comment':
        last_comment = code[node.start_byte:node.end_byte].decode('utf8')
    elif node.type in ['struct_specifier', 'preproc_function_def', 'preproc_def', 'enum_specifier', 'union_specifier', 'type_definition']:
        #print(node.type)
        node_type, node_text, node_comment, tokenized_node, tokenized_comment = extract_info_from_node(node, code, last_comment)
        print(f'Node Type: {node_type}')
        print(f'Node Text: {node_text}')
        if node_comment:
            print(f'Comments: {node_comment}')
            print(f'Tokenized Comments: {tokenized_comment}')
        else:
            print('Comments: None')
        print(f'Tokenized Node: {tokenized_node}')
        print('---')
        last_comment = None  # Reset last_comment afte
