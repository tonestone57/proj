import ast
import os

def check_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    try:
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, e

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            is_valid, error = check_file(filepath)
            if not is_valid:
                print(f"{filepath}: {error}")
