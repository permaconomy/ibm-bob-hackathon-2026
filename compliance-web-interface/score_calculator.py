"""
Score Calculator - Calculates compliance score based on violations
"""

def get_grade(score):
    """
    Return letter grade based on numerical score.
    """
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def calculate_score(violations):
    """
    Calculate compliance score based on violations.
    
    Args:
        violations: List of violation dicts, each with a 'severity' key
    
    Returns:
        int: Score from 0-100
    """
    # Start with perfect score
    score = 100
    
    # Deduct points based on severity
    severity_points = {
        "high": 5,
        "medium": 3,
        "low": 1
    }
    
    for violation in violations:
        severity = violation.get('severity', 'low').lower()
        points = severity_points.get(severity, 1)
        score -= points
    
    # Ensure score doesn't go below 0
    return max(0, score)


# For testing directly
if __name__ == "__main__":
    # Test the calculator
    test_violations = [
        {"severity": "high"},
        {"severity": "high"},
        {"severity": "medium"},
        {"severity": "low"}
    ]
    
    score = calculate_score(test_violations)
    grade = get_grade(score)
    print(f"Test violations: {len(test_violations)}")
    print(f"Score: {score}/100")
    print(f"Grade: {grade}")