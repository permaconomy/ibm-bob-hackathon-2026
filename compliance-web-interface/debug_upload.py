"""Debug script to test the entire upload and analysis flow"""
import os
import sys
import zipfile
import tempfile

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from evaluator_integration import analyze_submission

print("=" * 60)
print("DEBUG: Testing Upload and Analysis Flow")
print("=" * 60)

# Create a test ZIP file with Python code
test_dir = tempfile.mkdtemp(prefix='test_submission_')
print(f"\n1. Created temp directory: {test_dir}")

# Create some test Python files
test_files = {
    'main.py': '''
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

password = "hardcoded123"  # This should be detected
result = calculate_sum([1, 2, 3, 4, 5])
print(result)
''',
    'utils.py': '''
import os
import sys
import json  # unused import

def process_data(data):
    # TODO: Implement this function
    pass

def long_function():
    x = 1
    if x > 0:
        if x < 10:
            if x == 1:
                if True:
                    if False:
                        print("deeply nested")  # Deep nesting
    return x
'''
}

for filename, content in test_files.items():
    filepath = os.path.join(test_dir, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"   Created: {filename}")

# Create ZIP file
zip_path = os.path.join(tempfile.gettempdir(), 'test_submission.zip')
with zipfile.ZipFile(zip_path, 'w') as zipf:
    for filename in test_files.keys():
        filepath = os.path.join(test_dir, filename)
        zipf.write(filepath, filename)

print(f"\n2. Created ZIP file: {zip_path}")
print(f"   ZIP size: {os.path.getsize(zip_path)} bytes")

# Test analysis
print("\n3. Running analysis...")
print("-" * 60)

try:
    result = analyze_submission(zip_path, include_advanced=False)
    
    print("\n4. Analysis Results:")
    print("-" * 60)
    print(f"Status: {result.get('status')}")
    print(f"Score: {result.get('score')}")
    print(f"Grade: {result.get('grade')}")
    print(f"Total Files: {result.get('total_files')}")
    print(f"Files Scanned: {result.get('files_scanned')}")
    print(f"Total Violations: {result.get('total_violations')}")
    
    if result.get('severity_counts'):
        print(f"\nSeverity Counts:")
        for severity, count in result['severity_counts'].items():
            print(f"  {severity}: {count}")
    
    if result.get('detailed_analysis'):
        print(f"\nDetailed Analysis:")
        for category, count in result['detailed_analysis'].items():
            print(f"  {category}: {count}")
    
    if result.get('violations'):
        print(f"\nFirst 5 Violations:")
        for i, v in enumerate(result['violations'][:5], 1):
            print(f"  {i}. [{v.get('severity')}] {v.get('message')}")
            print(f"     File: {v.get('file')}, Line: {v.get('line')}")
    
    if result.get('recommendations'):
        print(f"\nRecommendations:")
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"  {i}. {rec}")
    
    print("\n" + "=" * 60)
    print("SUCCESS: Analysis completed!")
    print("=" * 60)
    
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Cleanup
    import shutil
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir, ignore_errors=True)
    if os.path.exists(zip_path):
        os.remove(zip_path)
    print("\nCleaned up test files")

# Made with Bob
