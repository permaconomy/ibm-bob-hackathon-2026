"""
IBM Bob May 2026 Hackathon Compliance Checker - Flask Web Application

Validates hackathon submissions against 8 red flags for IBM Bob Dev Day Hackathon May 2026.

This application uses Flask (BSD-3-Clause) and Werkzeug (BSD-3-Clause).
See THIRD-PARTY-LICENSES.txt for full license texts.

Copyright (c) 2026 AI Compliance Evaluator Team
Built with IBM Bob IDE for IBM Bob Dev Day Hackathon May 2026
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import time
import random
from datetime import datetime
from werkzeug.utils import secure_filename  # BSD-3-Clause licensed
import io
from evaluator_integration import analyze_submission

app = Flask(__name__)
# Use environment variable for production, fallback to random key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Disable template caching in development
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store mock results in memory (in production, use a database)
mock_results = {}

def generate_mock_results(submission_id):
    """Generate realistic mock validation results for 8 red flags"""
    
    # Randomly determine pass/fail for each red flag
    red_flags_status = {
        'bob_sessions': random.choice(['pass', 'fail']),
        'credentials': random.choice(['pass', 'fail']),
        'banned_models': random.choice(['pass', 'pass', 'fail']),  # More likely to pass
        'team_roster': random.choice(['pass', 'fail']),
        'timestamp': random.choice(['pass', 'pass', 'pass', 'fail']),  # More likely to pass
        'video': random.choice(['pass', 'fail']),
        'deliverables': random.choice(['pass', 'fail']),
        'personal_info': random.choice(['pass', 'pass', 'fail'])  # More likely to pass
    }
    
    # Calculate overall pass/fail (must pass all 8)
    overall_status = 'pass' if all(status == 'pass' for status in red_flags_status.values()) else 'fail'
    passed_count = sum(1 for status in red_flags_status.values() if status == 'pass')
    
    return {
        'submission_id': submission_id,
        'status': 'completed',
        'timestamp': datetime.now().isoformat(),
        'deadline': '2026-05-03T10:00:00-04:00',
        'overall_status': overall_status,
        'passed_flags': passed_count,
        'total_flags': 8,
        'total_files': random.randint(15, 45),
        'files_scanned': random.randint(15, 45),
        'red_flags': {
            '1_bob_sessions': {
                'name': 'bob_sessions Folder Check',
                'status': red_flags_status['bob_sessions'],
                'description': 'Validates IBM Bob IDE usage documentation',
                'details': [
                    {'finding': 'bob_sessions folder found' if red_flags_status['bob_sessions'] == 'pass' else 'bob_sessions folder missing',
                     'severity': 'pass' if red_flags_status['bob_sessions'] == 'pass' else 'critical'},
                    {'finding': 'Valid export format detected' if red_flags_status['bob_sessions'] == 'pass' else 'Invalid or missing export files',
                     'severity': 'pass' if red_flags_status['bob_sessions'] == 'pass' else 'high'}
                ]
            },
            '2_credentials': {
                'name': 'Exposed Credentials Scan',
                'status': red_flags_status['credentials'],
                'description': 'Detects exposed API keys, passwords, and tokens',
                'details': [
                    {'finding': 'No exposed credentials found' if red_flags_status['credentials'] == 'pass' else 'Found hardcoded API key in config.py',
                     'severity': 'pass' if red_flags_status['credentials'] == 'pass' else 'critical'},
                    {'finding': 'Environment variables used correctly' if red_flags_status['credentials'] == 'pass' else 'Password found in database.py line 45',
                     'severity': 'pass' if red_flags_status['credentials'] == 'pass' else 'critical'}
                ]
            },
            '3_banned_models': {
                'name': 'Banned AI Models Check',
                'status': red_flags_status['banned_models'],
                'description': 'Checks for prohibited AI tool usage',
                'details': [
                    {'finding': 'No banned AI models detected' if red_flags_status['banned_models'] == 'pass' else 'Reference to ChatGPT found in comments',
                     'severity': 'pass' if red_flags_status['banned_models'] == 'pass' else 'critical'},
                    {'finding': 'Only IBM Bob IDE usage detected' if red_flags_status['banned_models'] == 'pass' else 'Claude API call found in utils.py',
                     'severity': 'pass' if red_flags_status['banned_models'] == 'pass' else 'critical'}
                ]
            },
            '4_team_roster': {
                'name': 'Team Roster Validation',
                'status': red_flags_status['team_roster'],
                'description': 'Ensures maximum 5 members, no duplicates',
                'details': [
                    {'finding': 'Team size: 4 members (valid)' if red_flags_status['team_roster'] == 'pass' else 'Team size: 6 members (exceeds limit)',
                     'severity': 'pass' if red_flags_status['team_roster'] == 'pass' else 'critical'},
                    {'finding': 'No duplicate members found' if red_flags_status['team_roster'] == 'pass' else 'Duplicate member detected',
                     'severity': 'pass' if red_flags_status['team_roster'] == 'pass' else 'high'}
                ]
            },
            '5_timestamp': {
                'name': 'Timestamp Validation',
                'status': red_flags_status['timestamp'],
                'description': 'Validates submission before May 3, 2026 deadline',
                'details': [
                    {'finding': 'All files modified before deadline' if red_flags_status['timestamp'] == 'pass' else 'Files modified after May 3, 2026 10:00 AM ET',
                     'severity': 'pass' if red_flags_status['timestamp'] == 'pass' else 'critical'},
                    {'finding': 'Submission timestamp valid' if red_flags_status['timestamp'] == 'pass' else 'Late submission detected',
                     'severity': 'pass' if red_flags_status['timestamp'] == 'pass' else 'critical'}
                ]
            },
            '6_video': {
                'name': 'Video Presence Check',
                'status': red_flags_status['video'],
                'description': 'Confirms required demo video',
                'details': [
                    {'finding': 'Demo video found: demo.mp4' if red_flags_status['video'] == 'pass' else 'No video file found in submission',
                     'severity': 'pass' if red_flags_status['video'] == 'pass' else 'critical'},
                    {'finding': 'Video format valid (MP4)' if red_flags_status['video'] == 'pass' else 'Required demo video missing',
                     'severity': 'pass' if red_flags_status['video'] == 'pass' else 'critical'}
                ]
            },
            '7_deliverables': {
                'name': 'Deliverables Completeness',
                'status': red_flags_status['deliverables'],
                'description': 'Verifies all 4 required components',
                'details': [
                    {'finding': 'All 4 deliverables present' if red_flags_status['deliverables'] == 'pass' else 'Missing deliverable: Technical documentation',
                     'severity': 'pass' if red_flags_status['deliverables'] == 'pass' else 'critical'},
                    {'finding': 'README.md found and complete' if red_flags_status['deliverables'] == 'pass' else 'README.md incomplete or missing',
                     'severity': 'pass' if red_flags_status['deliverables'] == 'pass' else 'high'}
                ]
            },
            '8_personal_info': {
                'name': 'Personal Information Scan',
                'status': red_flags_status['personal_info'],
                'description': 'Detects PI data and social media scrapes',
                'details': [
                    {'finding': 'No personal information detected' if red_flags_status['personal_info'] == 'pass' else 'Social security numbers found in data.csv',
                     'severity': 'pass' if red_flags_status['personal_info'] == 'pass' else 'critical'},
                    {'finding': 'No social media scraping detected' if red_flags_status['personal_info'] == 'pass' else 'Twitter scraping code found in scraper.py',
                     'severity': 'pass' if red_flags_status['personal_info'] == 'pass' else 'high'}
                ]
            }
        },
        'recommendations': [
            'Ensure bob_sessions folder contains valid IBM Bob IDE exports' if red_flags_status['bob_sessions'] == 'fail' else None,
            'Remove all hardcoded credentials and use environment variables' if red_flags_status['credentials'] == 'fail' else None,
            'Remove references to banned AI models (ChatGPT, Claude, Gemini)' if red_flags_status['banned_models'] == 'fail' else None,
            'Reduce team size to maximum 5 members' if red_flags_status['team_roster'] == 'fail' else None,
            'Ensure all files are modified before May 3, 2026 10:00 AM ET' if red_flags_status['timestamp'] == 'fail' else None,
            'Include required demo video in submission' if red_flags_status['video'] == 'fail' else None,
            'Complete all 4 required deliverables' if red_flags_status['deliverables'] == 'fail' else None,
            'Remove personal information and social media scrapes' if red_flags_status['personal_info'] == 'fail' else None,
        ]
    }
    
    # Build the complete result
    result = {
        'submission_id': submission_id,
        'status': 'completed',
        'timestamp': datetime.now().isoformat(),
        'deadline': '2026-05-03T10:00:00-04:00',
        'overall_status': overall_status,
        'passed_flags': passed_count,
        'total_flags': 8,
        'total_files': random.randint(15, 45),
        'files_scanned': random.randint(15, 45),
        'red_flags': {
            '1_bob_sessions': {
                'name': 'bob_sessions Folder Check',
                'status': red_flags_status['bob_sessions'],
                'description': 'Validates IBM Bob IDE usage documentation',
                'details': [
                    {'finding': 'bob_sessions folder found' if red_flags_status['bob_sessions'] == 'pass' else 'bob_sessions folder missing',
                     'severity': 'pass' if red_flags_status['bob_sessions'] == 'pass' else 'critical'},
                    {'finding': 'Valid export format detected' if red_flags_status['bob_sessions'] == 'pass' else 'Invalid or missing export files',
                     'severity': 'pass' if red_flags_status['bob_sessions'] == 'pass' else 'high'}
                ]
            },
            '2_credentials': {
                'name': 'Exposed Credentials Scan',
                'status': red_flags_status['credentials'],
                'description': 'Detects exposed API keys, passwords, and tokens',
                'details': [
                    {'finding': 'No exposed credentials found' if red_flags_status['credentials'] == 'pass' else 'Found hardcoded API key in config.py',
                     'severity': 'pass' if red_flags_status['credentials'] == 'pass' else 'critical'},
                    {'finding': 'Environment variables used correctly' if red_flags_status['credentials'] == 'pass' else 'Password found in database.py line 45',
                     'severity': 'pass' if red_flags_status['credentials'] == 'pass' else 'critical'}
                ]
            },
            '3_banned_models': {
                'name': 'Banned AI Models Check',
                'status': red_flags_status['banned_models'],
                'description': 'Checks for prohibited AI tool usage',
                'details': [
                    {'finding': 'No banned AI models detected' if red_flags_status['banned_models'] == 'pass' else 'Reference to ChatGPT found in comments',
                     'severity': 'pass' if red_flags_status['banned_models'] == 'pass' else 'critical'},
                    {'finding': 'Only IBM Bob IDE usage detected' if red_flags_status['banned_models'] == 'pass' else 'Claude API call found in utils.py',
                     'severity': 'pass' if red_flags_status['banned_models'] == 'pass' else 'critical'}
                ]
            },
            '4_team_roster': {
                'name': 'Team Roster Validation',
                'status': red_flags_status['team_roster'],
                'description': 'Ensures maximum 5 members, no duplicates',
                'details': [
                    {'finding': 'Team size: 4 members (valid)' if red_flags_status['team_roster'] == 'pass' else 'Team size: 6 members (exceeds limit)',
                     'severity': 'pass' if red_flags_status['team_roster'] == 'pass' else 'critical'},
                    {'finding': 'No duplicate members found' if red_flags_status['team_roster'] == 'pass' else 'Duplicate member detected',
                     'severity': 'pass' if red_flags_status['team_roster'] == 'pass' else 'high'}
                ]
            },
            '5_timestamp': {
                'name': 'Timestamp Validation',
                'status': red_flags_status['timestamp'],
                'description': 'Validates submission before May 3, 2026 deadline',
                'details': [
                    {'finding': 'All files modified before deadline' if red_flags_status['timestamp'] == 'pass' else 'Files modified after May 3, 2026 10:00 AM ET',
                     'severity': 'pass' if red_flags_status['timestamp'] == 'pass' else 'critical'},
                    {'finding': 'Submission timestamp valid' if red_flags_status['timestamp'] == 'pass' else 'Late submission detected',
                     'severity': 'pass' if red_flags_status['timestamp'] == 'pass' else 'critical'}
                ]
            },
            '6_video': {
                'name': 'Video Presence Check',
                'status': red_flags_status['video'],
                'description': 'Confirms required demo video',
                'details': [
                    {'finding': 'Demo video found: demo.mp4' if red_flags_status['video'] == 'pass' else 'No video file found in submission',
                     'severity': 'pass' if red_flags_status['video'] == 'pass' else 'critical'},
                    {'finding': 'Video format valid (MP4)' if red_flags_status['video'] == 'pass' else 'Required demo video missing',
                     'severity': 'pass' if red_flags_status['video'] == 'pass' else 'critical'}
                ]
            },
            '7_deliverables': {
                'name': 'Deliverables Completeness',
                'status': red_flags_status['deliverables'],
                'description': 'Verifies all 4 required components',
                'details': [
                    {'finding': 'All 4 deliverables present' if red_flags_status['deliverables'] == 'pass' else 'Missing deliverable: Technical documentation',
                     'severity': 'pass' if red_flags_status['deliverables'] == 'pass' else 'critical'},
                    {'finding': 'README.md found and complete' if red_flags_status['deliverables'] == 'pass' else 'README.md incomplete or missing',
                     'severity': 'pass' if red_flags_status['deliverables'] == 'pass' else 'high'}
                ]
            },
            '8_personal_info': {
                'name': 'Personal Information Scan',
                'status': red_flags_status['personal_info'],
                'description': 'Detects PI data and social media scrapes',
                'details': [
                    {'finding': 'No personal information detected' if red_flags_status['personal_info'] == 'pass' else 'Social security numbers found in data.csv',
                     'severity': 'pass' if red_flags_status['personal_info'] == 'pass' else 'critical'},
                    {'finding': 'No social media scraping detected' if red_flags_status['personal_info'] == 'pass' else 'Twitter scraping code found in scraper.py',
                     'severity': 'pass' if red_flags_status['personal_info'] == 'pass' else 'high'}
                ]
            }
        }
    }
    
    # Add recommendations based on failures
    recommendations = []
    if red_flags_status['bob_sessions'] == 'fail':
        recommendations.append('Ensure bob_sessions folder contains valid IBM Bob IDE exports')
    if red_flags_status['credentials'] == 'fail':
        recommendations.append('Remove all hardcoded credentials and use environment variables')
    if red_flags_status['banned_models'] == 'fail':
        recommendations.append('Remove references to banned AI models (ChatGPT, Claude, Gemini)')
    if red_flags_status['team_roster'] == 'fail':
        recommendations.append('Reduce team size to maximum 5 members or remove duplicate members')
    if red_flags_status['timestamp'] == 'fail':
        recommendations.append('Ensure all files are modified before May 3, 2026 10:00 AM ET')
    if red_flags_status['video'] == 'fail':
        recommendations.append('Include required demo video in submission')
    if red_flags_status['deliverables'] == 'fail':
        recommendations.append('Complete all 4 required deliverables')
    if red_flags_status['personal_info'] == 'fail':
        recommendations.append('Remove personal information and social media scrapes from submission')
    
    if not recommendations:
        recommendations.append('All validation checks passed! Submission is compliant.')
    
    result['recommendations'] = recommendations
    return result

@app.route('/')
def home():
    """Home page"""
    return render_template('home.html')

@app.route('/upload')
def upload():
    """Upload page"""
    return render_template('upload.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """Handle file upload and return submission ID"""
    print("\n" + "="*60)
    print("[UPLOAD] Received upload request")
    print("="*60)
    
    try:
        # Check if file is present
        print("[UPLOAD] Checking for file in request...")
        if 'file' not in request.files:
            print("[ERROR] No file in request.files")
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        print(f"[UPLOAD] File object received: {file}")
        print(f"[UPLOAD] Filename: {file.filename}")
        
        if file.filename == '':
            print("[ERROR] Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        allowed_extensions = {'.zip', '.rar', '.py', '.js', '.java', '.cpp', '.c', '.go', '.rb', '.php'}
        file_ext = os.path.splitext(file.filename or '')[1].lower()
        print(f"[UPLOAD] File extension: {file_ext}")
        
        if file_ext not in allowed_extensions:
            print(f"[ERROR] File type not allowed: {file_ext}")
            return jsonify({'error': f'File type {file_ext} not allowed'}), 400
        
        # Save file
        filename = secure_filename(file.filename or 'upload')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"[UPLOAD] Saving to: {filepath}")
        file.save(filepath)
        print(f"[UPLOAD] File saved successfully")
        
        # Generate submission ID
        submission_id = f"SUB-{int(time.time())}-{random.randint(1000, 9999)}"
        
        # Check if advanced analysis is requested
        include_advanced = request.form.get('advanced', 'false').lower() == 'true'
        
        # Run REAL evaluator analysis instead of mock results
        try:
            analysis_results = analyze_submission(filepath, include_advanced=include_advanced)
            analysis_results['submission_id'] = submission_id
            analysis_results['timestamp'] = datetime.now().isoformat()
            mock_results[submission_id] = analysis_results
            print(f"[SUCCESS] Analysis completed for {submission_id}")
            print(f"  Score: {analysis_results.get('score')}")
            print(f"  Files: {analysis_results.get('total_files')}")
            print(f"  Violations: {analysis_results.get('total_violations')}")
        except Exception as analysis_error:
            # If analysis fails, store error result and PRINT IT
            import traceback
            print(f"\n[ERROR] Analysis failed for {submission_id}:")
            print(f"  Error: {str(analysis_error)}")
            print(f"  File: {filepath}")
            print("\nFull traceback:")
            traceback.print_exc()
            print()
            
            mock_results[submission_id] = {
                'submission_id': submission_id,
                'status': 'error',
                'error': str(analysis_error),
                'message': f'Analysis failed: {str(analysis_error)}'
            }
        
        return jsonify({
            'success': True,
            'submission_id': submission_id,
            'message': 'File uploaded and analyzed successfully',
            'advanced_analysis': include_advanced
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/results/<submission_id>')
def results(submission_id):
    """Results page - V2 with fixed JavaScript"""
    return render_template('results_v2.html', submission_id=submission_id)

@app.route('/api/results/<submission_id>')
def api_results(submission_id):
    """Get results for a submission"""
    if submission_id in mock_results:
        return jsonify(mock_results[submission_id])
    else:
        return jsonify({
            'status': 'processing',
            'message': 'Analysis in progress...'
        })

@app.route('/api/download/<submission_id>')
def download_report(submission_id):
    """Download compliance report as JSON"""
    if submission_id not in mock_results:
        return jsonify({'error': 'Results not found'}), 404
    
    # Create JSON report
    report = mock_results[submission_id]
    report_json = json.dumps(report, indent=2)
    
    # Create file-like object
    buffer = io.BytesIO()
    buffer.write(report_json.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'compliance_report_{submission_id}.json',
        mimetype='application/json'
    )

if __name__ == '__main__':
    # Get port from environment variable (IBM Cloud sets this) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Disable debug mode in production
    debug_mode = os.environ.get('FLASK_ENV', 'production') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

# Made with Bob
