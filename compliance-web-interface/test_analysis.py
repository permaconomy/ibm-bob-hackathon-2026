"""Quick test to verify analysis is working"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from evaluator_integration import analyze_submission

# Create a simple test file
test_file = 'test_sample.py'
with open(test_file, 'w') as f:
    f.write('print("hello world")\n')

print("Testing analysis...")
try:
    result = analyze_submission(test_file)
    print("\n[OK] Analysis completed!")
    print(f"Status: {result.get('status')}")
    print(f"Score: {result.get('score')}")
    print(f"Grade: {result.get('grade')}")
    print(f"Total Files: {result.get('total_files')}")
    print(f"Total Violations: {result.get('total_violations')}")
    print(f"\nResult keys: {list(result.keys())}")
    
    if result.get('recommendations'):
        print(f"\nRecommendations ({len(result['recommendations'])}):")
        for rec in result['recommendations'][:3]:
            print(f"  - {rec}")
    
except Exception as e:
    print(f"\n[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"\nCleaned up {test_file}")

# Made with Bob
