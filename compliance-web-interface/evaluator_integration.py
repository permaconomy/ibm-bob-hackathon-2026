"""
Evaluator Integration Module
Bridges the code compliance evaluator engine with the web interface
Supports both basic code quality checks and advanced hackathon compliance
"""

import os
import tempfile
import zipfile
import shutil
from pathlib import Path

# Try to import rarfile for RAR support
try:
    import rarfile
    RAR_SUPPORT = True
except ImportError:
    RAR_SUPPORT = False
from scanner import scan_directory, scan_single_file
from score_calculator import calculate_score, get_grade
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

# Import advanced compliance checker (optional, seamless integration)
try:
    from advanced_compliance_checker import analyze_advanced_compliance
    ADVANCED_CHECKER_AVAILABLE = True
except ImportError:
    ADVANCED_CHECKER_AVAILABLE = False


def extract_archive_to_temp(archive_path):
    """
    Extract uploaded ZIP or RAR file to temporary directory
    Returns the temporary directory path
    """
    temp_dir = tempfile.mkdtemp(prefix='compliance_scan_')
    file_ext = os.path.splitext(archive_path)[1].lower()
    
    try:
        if file_ext == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
        elif file_ext == '.rar':
            if not RAR_SUPPORT:
                raise Exception("RAR support not available. Please install rarfile: pip install rarfile")
            with rarfile.RarFile(archive_path, 'r') as rar_ref:
                rar_ref.extractall(temp_dir)
        else:
            raise Exception(f"Unsupported archive format: {file_ext}")
        
        return temp_dir
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise Exception(f"Failed to extract archive file: {str(e)}")


def extract_zip_to_temp(zip_path):
    """
    Legacy function for backward compatibility
    Extract uploaded ZIP file to temporary directory
    Returns the temporary directory path
    """
    return extract_archive_to_temp(zip_path)


def analyze_submission(file_path, include_advanced=False):
    """
    Analyze uploaded submission file
    Returns detailed compliance results
    
    Args:
        file_path: Path to uploaded file (ZIP or single code file)
        include_advanced: If True, run advanced hackathon compliance checks
    
    Returns:
        dict: Comprehensive analysis results
    """
    temp_dir = None
    
    try:
        # Determine if it's an archive file (ZIP/RAR) or single file
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in ['.zip', '.rar']:
            # Extract archive to temp directory
            temp_dir = extract_archive_to_temp(file_path)
            scan_path = temp_dir
            is_directory = True
        else:
            # Single file scan
            scan_path = file_path
            is_directory = False
        
        # Run the scan
        if is_directory:
            violations = scan_directory(scan_path)
        else:
            violations = scan_single_file(scan_path)
        
        # Calculate score and grade
        score = calculate_score(violations)
        grade = get_grade(score)
        
        # Count files scanned
        if is_directory:
            total_files = sum(1 for _ in Path(scan_path).rglob('*') 
                            if _.is_file() and _.suffix in ['.py', '.js', '.java', '.cpp', '.c'])
        else:
            total_files = 1
        
        # Organize violations by severity
        severity_counts = {'high': 0, 'medium': 0, 'low': 0}
        violations_by_file = {}
        
        for violation in violations:
            severity = violation.get('severity', 'low').lower()
            if severity in severity_counts:
                severity_counts[severity] += 1
            
            file_name = violation.get('file', 'unknown')
            if file_name not in violations_by_file:
                violations_by_file[file_name] = []
            violations_by_file[file_name].append(violation)
        
        # Determine overall status
        overall_status = 'pass' if score >= 70 else 'fail'
        
        # Generate recommendations
        recommendations = generate_recommendations(violations, score, grade)
        
        # Build result structure
        result = {
            'status': 'completed',
            'overall_status': overall_status,
            'score': score,
            'grade': grade,
            'total_violations': len(violations),
            'total_files': total_files,
            'files_scanned': total_files,
            'severity_counts': severity_counts,
            'violations': violations[:50],  # Limit to first 50 for display
            'violations_by_file': {k: v[:10] for k, v in list(violations_by_file.items())[:10]},  # Top 10 files
            'recommendations': recommendations,
            'detailed_analysis': {
                'hardcoded_secrets': count_violation_type(violations, 'secret'),
                'sql_injection': count_violation_type(violations, 'SQL injection'),
                'missing_error_handling': count_violation_type(violations, 'try/except'),
                'dangerous_functions': count_violation_type(violations, 'eval'),
                'long_functions': count_violation_type(violations, 'lines long'),
                'deep_nesting': count_violation_type(violations, 'Nesting level'),
                'todo_comments': count_violation_type(violations, 'TODO'),
                'unused_imports': count_violation_type(violations, 'Unused import')
            }
        }
        
        # Add advanced compliance report if requested and available
        if include_advanced and ADVANCED_CHECKER_AVAILABLE:
            try:
                # Run advanced compliance check on the scan path
                advanced_report = analyze_advanced_compliance(scan_path)
                result['advanced_compliance'] = advanced_report
                result['has_advanced_report'] = True
            except Exception as e:
                result['advanced_compliance'] = {
                    'status': 'error',
                    'message': f'Advanced check failed: {str(e)}'
                }
                result['has_advanced_report'] = False
        else:
            result['has_advanced_report'] = False
        
        return result
    
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'message': f'Analysis failed: {str(e)}'
        }
    
    finally:
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)


def count_violation_type(violations, keyword):
    """Count violations containing a specific keyword"""
    count = 0
    for v in violations:
        message = v.get('message', '').lower()
        if keyword.lower() in message:
            count += 1
    return count


def generate_recommendations(violations, score, grade):
    """Generate actionable recommendations based on violations"""
    recommendations = []
    
    # Check for specific violation types
    has_secrets = any('secret' in v.get('message', '').lower() or 
                     'password' in v.get('message', '').lower() or
                     'api' in v.get('message', '').lower() 
                     for v in violations)
    
    has_sql = any('sql' in v.get('message', '').lower() for v in violations)
    has_eval = any('eval' in v.get('message', '').lower() or 
                   'exec' in v.get('message', '').lower() 
                   for v in violations)
    has_error_handling = any('try/except' in v.get('message', '').lower() for v in violations)
    has_long_functions = any('lines long' in v.get('message', '').lower() for v in violations)
    has_deep_nesting = any('nesting' in v.get('message', '').lower() for v in violations)
    
    if has_secrets:
        recommendations.append('🔴 CRITICAL: Remove all hardcoded credentials. Use environment variables or secure vaults.')
    
    if has_sql:
        recommendations.append('🔴 CRITICAL: Fix SQL injection vulnerabilities. Use parameterized queries.')
    
    if has_eval:
        recommendations.append('🔴 CRITICAL: Remove eval() and exec() functions. They pose serious security risks.')
    
    if has_error_handling:
        recommendations.append('🟡 Add try/except blocks around risky operations (file I/O, network calls, parsing).')
    
    if has_long_functions:
        recommendations.append('🟡 Refactor long functions (>50 lines) into smaller, more maintainable units.')
    
    if has_deep_nesting:
        recommendations.append('🟢 Reduce nesting depth. Consider early returns or extracting nested logic.')
    
    # Grade-based recommendations
    if grade == 'F':
        recommendations.append('❌ URGENT: Critical issues detected. Address high-severity violations immediately.')
    elif grade == 'D':
        recommendations.append('⚠️ Multiple issues found. Focus on high and medium severity violations first.')
    elif grade == 'C':
        recommendations.append('👍 Fair score. Address remaining medium severity issues to improve quality.')
    elif grade == 'B':
        recommendations.append('✅ Good work! Minor improvements will bring you to excellent quality.')
    else:  # Grade A
        recommendations.append('🎉 Excellent! Your code meets high compliance standards.')
    
    if not recommendations:
        recommendations.append('✅ No major issues detected. Code quality is acceptable.')
    
    return recommendations


def format_violation_for_display(violation):
    """Format a violation for web display"""
    return {
        'file': os.path.basename(violation.get('file', 'unknown')),
        'line': violation.get('line', 0),
        'message': violation.get('message', 'Unknown violation'),
        'severity': violation.get('severity', 'low'),
        'severity_icon': get_severity_icon(violation.get('severity', 'low'))
    }


def get_severity_icon(severity):
    """Get emoji icon for severity level"""
    severity_lower = severity.lower()
    if severity_lower == 'high' or severity_lower == 'critical':
        return '🔴'
    elif severity_lower == 'medium':
        return '🟡'
    else:
        return '🟢'

# Made with Bob
