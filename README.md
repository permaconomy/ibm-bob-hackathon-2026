# 🎯 AI Compliance Evaluator - IBM Bob Dev Day Hackathon May 2026

A comprehensive compliance validation system for hackathon submissions, featuring automated checks against 8 critical red flags. Built entirely using IBM Bob IDE with both a powerful evaluation engine and an intuitive web interface.

## 🌟 Overview

This project validates hackathon submissions against strict compliance requirements, including:
- ✅ IBM Bob IDE usage verification (`bob_sessions` folder)
- ✅ Exposed credentials detection
- ✅ Banned AI model scanning
- ✅ Team roster validation
- ✅ Deadline enforcement
- ✅ Video presence confirmation
- ✅ Deliverables completeness
- ✅ Personal information scanning

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Running the Web Interface

1. **Navigate to the web interface directory:**
   ```bash
   cd compliance-web-interface
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5000`

### Running the Evaluator Engine

1. **Navigate to the evaluator directory:**
   ```bash
   cd evaluator_program
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the evaluator:**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
ai-compliance-evaluator/
├── README.md                          # This file
├── PROBLEM_SOLUTION_STATEMENT.md      # Problem and solution overview
├── TECHNICAL_ARCHITECTURE.md          # Architecture documentation
├── GITHUB_ESSENTIAL_FILES.md          # File organization guide
├── bob_sessions/                      # IBM Bob IDE task sessions
│   ├── *.md                          # Task session exports
│   └── screenshots/                   # Session screenshots
├── compliance-web-interface/          # Web interface
│   ├── app.py                        # Flask application
│   ├── scanner.py                    # Code scanning logic
│   ├── score_calculator.py           # Scoring engine
│   ├── validators.py                 # Validation functions
│   ├── requirements.txt              # Python dependencies
│   ├── static/                       # CSS and JavaScript
│   ├── templates/                    # HTML templates
│   └── README.md                     # Web interface docs
└── evaluator_program/                 # Evaluation engine
    ├── main.py                       # Main evaluator
    ├── scanner.py                    # Scanning logic
    ├── score_calculator.py           # Score calculations
    ├── validators.py                 # Validation rules
    ├── requirements.txt              # Python dependencies
    └── README.md                     # Engine documentation
```

## 🎨 Features

### Web Interface
- **Modern UI**: Bootstrap 5-based responsive design
- **Drag & Drop Upload**: Easy file submission
- **Real-time Validation**: Instant compliance feedback
- **Detailed Reports**: Comprehensive results with recommendations
- **Mobile Responsive**: Works on all devices

### Evaluation Engine
- **8 Red Flags Validation**: Complete compliance checking
- **Credential Scanning**: Detects exposed API keys and secrets
- **Team Validation**: Ensures roster compliance
- **Timestamp Verification**: Deadline enforcement
- **Extensible Architecture**: Easy to add new validators

## 📖 Documentation

- **[PROBLEM_SOLUTION_STATEMENT.md](PROBLEM_SOLUTION_STATEMENT.md)** - Problem overview and solution approach
- **[TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md)** - System architecture and design
- **[compliance-web-interface/README.md](compliance-web-interface/README.md)** - Web interface documentation
- **[evaluator_program/README.md](evaluator_program/README.md)** - Evaluation engine documentation

## 🔍 IBM Bob IDE Usage Proof

This project demonstrates extensive use of IBM Bob IDE throughout development. The `bob_sessions/` folder contains:
- 9 complete task session exports (.md files)
- 9 screenshots documenting the development process
- Full conversation history showing Bob's assistance

This meta-validation proves our compliance with the hackathon's IBM Bob IDE usage requirement.

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask 3.0.0
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5.3.0
- **Validation**: Custom rule engine with regex patterns
- **Development**: IBM Bob IDE

## 🎯 Target Users

1. **Hackathon Participants**: Validate submissions before final upload
2. **Judges**: Quick compliance verification of submissions
3. **Organizers**: Automated pre-screening of entries

## 📝 License

This project was created for the IBM Bob Dev Day Hackathon May 2026.

Copyright (c) 2026 AI Compliance Evaluator Team

See [THIRD-PARTY-LICENSES.txt](compliance-web-interface/THIRD-PARTY-LICENSES.txt) for third-party library licenses.

## 🤝 Contributing

This is a hackathon submission project. For questions or issues, please contact the development team.

## 📞 Support

For setup issues:
1. Check the README in each component directory
2. Ensure Python 3.8+ is installed
3. Verify all dependencies are installed correctly

## 🎉 Acknowledgments

- IBM for hosting the Bob Dev Day Hackathon May 2026
- IBM Bob IDE for enabling rapid development
- Bootstrap team for the excellent CSS framework
- Flask team for the lightweight web framework

---

**Built with IBM Bob IDE for IBM Bob Dev Day Hackathon May 2026** 🚀