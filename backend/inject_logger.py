import os
import glob
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace standard logging with tracenest
    if 'import logging\nlogger = logging.getLogger(__name__)' in content:
        content = content.replace('import logging\nlogger = logging.getLogger(__name__)', 'from tracenest import logger')
    elif 'import logging' in content:
        content = re.sub(r'import logging\s*logger = logging\.getLogger\(__name__\)', 'from tracenest import logger', content)
        
    # If the file doesn't have tracenest logger, add it
    if 'from tracenest import logger' not in content:
        content = "from tracenest import logger\n" + content

    # 2. Inject logger.debug at function starts
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        # Check if line is a function definition
        match = re.match(r'^(\s*)(async\s+)?def\s+([a-zA-Z0-9_]+)\(', line)
        if match:
            indent = match.group(1)
            func_name = match.group(3)
            # Find the end of the signature
            j = i
            sig = line
            while j < len(lines) and not sig.rstrip().endswith(':'):
                j += 1
                sig += lines[j] if j < len(lines) else ""
            
            if j == i:
                # One line signature, we can inject on the next line
                inject = f'{indent}    logger.debug(f"Entering {func_name}")'
                new_lines.append(inject)
                
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

if __name__ == '__main__':
    for py_file in glob.glob('backend/app/**/*.py', recursive=True):
        if not py_file.endswith('__init__.py') and 'tests' not in py_file:
            print(f"Instrumenting {py_file}")
            try:
                process_file(py_file)
            except Exception as e:
                print(f"Failed {py_file}: {e}")
