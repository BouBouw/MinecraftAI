#!/usr/bin/env python3
"""
Fix Python imports for direct script execution
Changes relative imports to work when scripts are run directly
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix relative imports in a Python file"""
    with open(file_path, 'r') as f:
        content = f.read()

    original_content = content
    changes = []

    # Replace relative imports with absolute imports
    # from ..utils.config -> from llm.python.utils.config
    content = re.sub(r'from \.\.utils\.([^ ]+)', r'from llm.python.utils.\1', content)
    content = re.sub(r'from \.\.gym_env\.([^ ]+)', r'from llm.python.gym_env.\1', content)
    content = re.sub(r'from \.\.agents\.([^ ]+)', r'from llm.python.agents.\1', content)
    content = re.sub(r'from \.\.memory\.([^ ]+)', r'from llm.python.memory.\1', content)
    content = re.sub(r'from \.\.crafting\.([^ ]+)', r'from llm.python.crafting.\1', content)
    content = re.sub(r'from \.\.training\.([^ ]+)', r'from llm.python.training.\1', content)
    content = re.sub(r'from \.\.bridge\.([^ ]+)', r'from llm.python.bridge.\1', content)

    # Replace single dot imports
    content = re.sub(r'from \.utils', r'from llm.python.utils', content)
    content = re.sub(r'from \.gym_env', r'from llm.python.gym_env', content)
    content = re.sub(r'from \.agents', r'from llm.python.agents', content)
    content = re.sub(r'from \.memory', r'from llm.python.memory', content)
    content = re.sub(r'from \.crafting', r'from llm.python.crafting', content)
    content = re.sub(r'from \.training', r'from llm.python.training', content)
    content = re.sub(r'from \.bridge', r'from llm.python.bridge', content)

    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    """Fix all Python files in llm/python"""
    python_dir = Path('llm/python')

    if not python_dir.exists():
        print("Error: llm/python directory not found")
        return

    fixed_count = 0
    total_count = 0

    for py_file in python_dir.rglob('*.py'):
        total_count += 1
        if fix_imports_in_file(py_file):
            fixed_count += 1
            print(f"✅ Fixed: {py_file}")
        else:
            print(f"   OK: {py_file}")

    print(f"\n📊 Summary:")
    print(f"   Total files: {total_count}")
    print(f"   Fixed files: {fixed_count}")
    print(f"   Already OK: {total_count - fixed_count}")

if __name__ == '__main__':
    main()
