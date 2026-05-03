
"""
File Scanner - Scans directories and applies compliance validators
"""

import os
from validators import (
    detect_hardcoded_secrets,
    detect_sql_injection_risk,
    detect_missing_try_except,
    detect_eval_exec_usage,
    detect_long_functions,
    detect_deep_nesting,
    detect_todo_fixme_comments,
    detect_unused_imports
)

def scan_single_file(file_path):
    """
    Scan a single file using all validators
    Returns a list of violations
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            file_lines = f.readlines()
    except Exception as e:
        return [{
            "file": file_path,
            "line": 0,
            "message": f"Could not read file: {str(e)}",
            "severity": "medium"
        }]
    
    all_violations = []
    
    # List of all validators
    validators = [
        detect_hardcoded_secrets,
        detect_sql_injection_risk,
        detect_missing_try_except,
        detect_eval_exec_usage,
        detect_long_functions,
        detect_deep_nesting,
        detect_todo_fixme_comments,
        detect_unused_imports
    ]
    
    # Apply each validator
    for validator in validators:
        try:
            violations = validator(file_lines, file_path)
            for v in violations:
                v["file"] = file_path
                all_violations.append(v)
        except Exception as e:
            all_violations.append({
                "file": file_path,
                "line": 0,
                "message": f"Validator error: {str(e)}",
                "severity": "low"
            })
    
    return all_violations

def scan_directory(directory_path):
    """
    Scan all Python files in a directory recursively
    Returns a list of all violations
    """
    all_violations = []
    extensions = ['.py', '.js', '.java', '.cpp']
    
    if not os.path.exists(directory_path):
        return [{
            "file": directory_path,
            "line": 0,
            "message": f"Directory does not exist: {directory_path}",
            "severity": "high"
        }]
    
    for root, dirs, files in os.walk(directory_path):
        # Skip hidden directories and virtual environments
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and d != 'venv' and d != '.venv']
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                violations = scan_single_file(file_path)
                all_violations.extend(violations)
    
    return all_violations

# For testing directly
if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    results = scan_directory(path)
    print(f"Found {len(results)} violations")
    for r in results[:10]:
        print(f"{r.get('file', 'unknown')}:{r.get('line', 0)} - {r.get('message', '')}")