"""
validators.py - Code quality validators for detecting common red flags
"""

import re
import ast


def detect_hardcoded_secrets(file_lines, file_path):
    """Detect hardcoded secrets like passwords, API keys, tokens."""
    violations = []
    secret_patterns = [
        r'password\s*=\s*["\'].*["\']',
        r'api[_-]?key\s*=\s*["\'].*["\']',
        r'secret\s*=\s*["\'].*["\']',
        r'token\s*=\s*["\'].*["\']',
        r'auth\s*=\s*["\'].*["\']',
    ]
    
    for line_num, line in enumerate(file_lines, start=1):
        line_lower = line.lower()
        for pattern in secret_patterns:
            if re.search(pattern, line_lower, re.IGNORECASE):
                violations.append({
                    "line": line_num,
                    "message": f"Potential hardcoded secret detected: {line.strip()}",
                    "severity": "high"
                })
                break
    
    return violations


def detect_sql_injection_risk(file_lines, file_path):
    """Detect SQL injection risks from string concatenation in SQL queries."""
    violations = []
    sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE']
    
    for line_num, line in enumerate(file_lines, start=1):
        line_upper = line.upper()
        # Check if line contains SQL keywords and string concatenation
        has_sql = any(keyword in line_upper for keyword in sql_keywords)
        has_concat = ('+' in line or '%' in line or '.format(' in line or 'f"' in line or "f'" in line)
        
        if has_sql and has_concat and ('=' in line or 'WHERE' in line_upper):
            violations.append({
                "line": line_num,
                "message": "Potential SQL injection risk: string concatenation in SQL query",
                "severity": "high"
            })
    
    return violations


def detect_missing_try_except(file_lines, file_path):
    """Detect risky operations without try/except blocks."""
    violations = []
    risky_operations = [
        'open(',
        'requests.',
        'urllib.',
        'json.loads(',
        'json.load(',
        'int(',
        'float(',
        '.read(',
        '.write(',
    ]
    
    # Parse the file to understand try/except blocks
    try:
        file_content = ''.join(file_lines)
        tree = ast.parse(file_content)
        
        # Find all try blocks line ranges
        try_blocks = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                try_blocks.append((node.lineno, node.end_lineno))
        
        # Check for risky operations outside try blocks
        for line_num, line in enumerate(file_lines, start=1):
            # Skip if line is in a try block
            in_try_block = any(start <= line_num <= end for start, end in try_blocks)
            if in_try_block:
                continue
            
            # Check for risky operations
            for operation in risky_operations:
                if operation in line and not line.strip().startswith('#'):
                    violations.append({
                        "line": line_num,
                        "message": f"Risky operation '{operation}' without try/except block",
                        "severity": "medium"
                    })
                    break
    except SyntaxError:
        # If we can't parse, do basic check
        for line_num, line in enumerate(file_lines, start=1):
            for operation in risky_operations:
                if operation in line and not line.strip().startswith('#'):
                    violations.append({
                        "line": line_num,
                        "message": f"Risky operation '{operation}' - consider using try/except",
                        "severity": "medium"
                    })
                    break
    
    return violations


def detect_eval_exec_usage(file_lines, file_path):
    """Detect usage of eval() or exec() which are security risks."""
    violations = []
    dangerous_functions = ['eval(', 'exec(']
    
    for line_num, line in enumerate(file_lines, start=1):
        if line.strip().startswith('#'):
            continue
        
        for func in dangerous_functions:
            if func in line:
                violations.append({
                    "line": line_num,
                    "message": f"Dangerous function '{func[:-1]}()' detected - security risk",
                    "severity": "high"
                })
                break
    
    return violations


def detect_long_functions(file_lines, file_path):
    """Detect functions longer than 50 lines."""
    violations = []
    
    try:
        file_content = ''.join(file_lines)
        tree = ast.parse(file_content)
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.end_lineno and node.lineno:
                    func_length = node.end_lineno - node.lineno + 1
                    if func_length > 50:
                        violations.append({
                            "line": node.lineno,
                            "message": f"Function '{node.name}' is {func_length} lines long (max 50)",
                            "severity": "medium"
                        })
    except SyntaxError:
        pass
    
    return violations


def detect_deep_nesting(file_lines, file_path):
    """Detect nesting deeper than 4 levels."""
    violations = []
    
    for line_num, line in enumerate(file_lines, start=1):
        if line.strip() and not line.strip().startswith('#'):
            # Count leading spaces to determine indentation level
            leading_spaces = len(line) - len(line.lstrip())
            # Assuming 4 spaces per indent level
            indent_level = leading_spaces // 4
            
            if indent_level > 4:
                violations.append({
                    "line": line_num,
                    "message": f"Nesting level {indent_level} exceeds maximum of 4",
                    "severity": "medium"
                })
    
    return violations


def detect_todo_fixme_comments(file_lines, file_path):
    """Detect TODO/FIXME comments."""
    violations = []
    markers = ['TODO', 'FIXME', 'HACK', 'XXX']
    
    for line_num, line in enumerate(file_lines, start=1):
        line_upper = line.upper()
        for marker in markers:
            if marker in line_upper and '#' in line:
                violations.append({
                    "line": line_num,
                    "message": f"{marker} comment found: {line.strip()}",
                    "severity": "low"
                })
                break
    
    return violations


def detect_unused_imports(file_lines, file_path):
    """Detect unused imports."""
    violations = []
    
    try:
        file_content = ''.join(file_lines)
        tree = ast.parse(file_content)
        
        # Collect all imports
        imports = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    imports[name] = node.lineno
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    imports[name] = node.lineno
        
        # Check if imports are used
        for import_name, line_num in imports.items():
            # Simple heuristic: check if import name appears elsewhere in the file
            used = False
            for check_line_num, line in enumerate(file_lines, start=1):
                if check_line_num == line_num:
                    continue
                # Check if the import is referenced
                if import_name in line and not line.strip().startswith('import'):
                    used = True
                    break
            
            if not used:
                violations.append({
                    "line": line_num,
                    "message": f"Unused import: {import_name}",
                    "severity": "low"
                })
    except SyntaxError:
        pass
    
    return violations
