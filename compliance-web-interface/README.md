# 🎨 IBM Bob May 2026 Hackathon Compliance Checker - Web Interface

A modern, responsive web interface for validating hackathon submissions against all 8 red flags. Built with Flask, Bootstrap 5, and vanilla JavaScript using IBM Bob IDE.

## 📋 Features

- ✅ **8 Red Flags Validation** - Comprehensive check against all hackathon requirements
- ✅ **bob_sessions Folder Check** - Validates IBM Bob IDE usage documentation
- ✅ **Credential Scanning** - Detects exposed API keys, passwords, and tokens
- ✅ **Team Roster Validation** - Ensures maximum 5 members, no duplicates
- ✅ **Deadline Enforcement** - Validates submission before May 3, 2026, 10:00 AM ET
- ✅ **Video Presence Check** - Confirms required demo video
- ✅ **Deliverables Completeness** - Verifies all 4 required components
- ✅ **Personal Info Scan** - Detects PI data and social media scrapes
- ✅ **Interactive Results** - Animated scores, expandable sections, pass/fail status
- ✅ **Mobile Responsive** - Works perfectly on all devices
- ✅ **Download Reports** - Export validation results as JSON

## 🛠️ Tech Stack

- **Backend**: Flask 3.0.0 (Python)
- **Frontend**: Bootstrap 5.3.0, Vanilla JavaScript
- **Icons**: Bootstrap Icons
- **Styling**: Custom CSS with responsive design

## 📁 Project Structure

```
compliance-web-interface/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/
│   │   └── main.js       # JavaScript utilities
│   └── images/           # Image assets
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Home page
│   ├── upload.html       # Upload page
│   ├── results.html      # Results page
│   └── about.html        # About page
└── uploads/              # Uploaded files (created automatically)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Your complete hackathon submission as a ZIP file

### Installation

1. **Navigate to the project directory**
   ```bash
   cd compliance-web-interface
   ```

2. **Create a virtual environment**
   
   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **Mac/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   
   Navigate to: `http://localhost:5000`

### Automated Setup (Windows)

For Windows users, we provide automated setup scripts:

1. **Run the setup script:**
   ```bash
   setup.bat
   ```
   This will create a virtual environment and install all dependencies.

2. **Start the application:**
   ```bash
   start_app.bat
   ```
   This will activate the virtual environment and start the Flask server.

See `SETUP_INSTRUCTIONS.md` for detailed troubleshooting and manual setup steps.

### Using the Checker

1. **Prepare Your Submission:**
   - Ensure your submission includes all required components
   - Include the `bob_sessions` folder with IBM Bob IDE exports
   - Add your demo video
   - Include team roster and all deliverables

2. **Upload and Validate:**
   - Click "Upload Submission" on the home page
   - Drag and drop your ZIP file or click to browse
   - Wait for validation (typically <60 seconds)

3. **Review Results:**
   - Check pass/fail status for each of the 8 red flags
   - Review detailed findings and recommendations
   - Download the JSON report for your records

## 📖 Usage Guide

### 1. Home Page
- Overview of the 8 red flags validation system
- IBM Bob Dev Day Hackathon May 2026 context
- Deadline warning (May 3, 2026, 10:00 AM ET)
- Quick access to upload page
- Statistics: 8 Red Flags, 144 Compliance Rules, <60s scan time

### 2. Upload Page
- **Drag & Drop**: Drag your ZIP file directly onto the upload zone
- **Browse**: Click "Browse Files" to select your submission ZIP
- **Supported Format**: ZIP files only (complete hackathon submission)
- **Max Size**: 50MB per file
- **What to Include**: bob_sessions folder, video, deliverables, team roster

### 3. Results Page
- **Overall Pass/Fail Status**: Clear indication of submission compliance
- **8 Red Flags Breakdown**: Individual pass/fail for each validation point
  1. bob_sessions Folder Check
  2. Exposed Credentials Scan
  3. Banned AI Models Check
  4. Team Roster Validation
  5. Timestamp Validation
  6. Video Presence Check
  7. Deliverables Completeness
  8. Personal Information Scan
- **Detailed Findings**: Expandable sections with specific issues
- **Recommendations**: Actionable suggestions for fixing failures
- **Download Report**: Export validation results as JSON

### 4. About Page
- Detailed explanation of all 8 red flags
- Meta-validation architecture overview
- RAG-powered intelligence explanation
- Target users: participants and judges
- Technology stack information

## 🎨 Customization

### Changing Colors

Edit `static/css/style.css` and modify the CSS variables:

```css
:root {
    --primary-color: #0066cc;
    --secondary-color: #6c757d;
    --success-color: #198754;
    --danger-color: #dc3545;
    --warning-color: #ffc107;
    --info-color: #0dcaf0;
}
```

### Adding New Pages

1. Create a new HTML template in `templates/`
2. Add a route in `app.py`:
   ```python
   @app.route('/newpage')
   def newpage():
       return render_template('newpage.html')
   ```
3. Add navigation link in `templates/base.html`

## 🔌 Connecting to Real Validation Backend

Currently, the application uses mock data for demonstration. To integrate with the real 8 red flags validation engine:

### 1. Update API Endpoints in `app.py`

Replace the mock data generation with actual validation logic:

```python
import requests
import zipfile
import os

@app.route('/api/upload', methods=['POST'])
def api_upload():
    # Save and extract ZIP file
    file = request.files['file']
    filepath = save_file(file)
    extract_dir = extract_zip(filepath)
    
    # Run 8 red flags validation
    validation_results = {
        'bob_sessions': validate_bob_sessions(extract_dir),
        'credentials': scan_credentials(extract_dir),
        'banned_models': check_banned_models(extract_dir),
        'team_roster': validate_team_roster(extract_dir),
        'timestamp': validate_timestamp(extract_dir),
        'video': check_video_presence(extract_dir),
        'deliverables': check_deliverables(extract_dir),
        'personal_info': scan_personal_info(extract_dir)
    }
    
    return jsonify(validation_results)
```

### 2. Implement Validation Functions

Each red flag needs its own validation function:

```python
def validate_bob_sessions(extract_dir):
    """Check for bob_sessions folder and valid exports"""
    bob_sessions_path = os.path.join(extract_dir, 'bob_sessions')
    if not os.path.exists(bob_sessions_path):
        return {'status': 'fail', 'message': 'bob_sessions folder not found'}
    # Add more validation logic
    return {'status': 'pass', 'message': 'Valid bob_sessions found'}

def scan_credentials(extract_dir):
    """Scan for exposed API keys, passwords, tokens"""
    # Implement credential scanning logic
    pass

# Implement remaining validation functions...
```

### 3. Environment Variables

Create a `.env` file for configuration:

```env
BACKEND_API_URL=http://your-backend-api.com
API_KEY=your-api-key
SECRET_KEY=your-secret-key
DEADLINE_TIMESTAMP=2026-05-03T10:00:00-04:00
MAX_TEAM_SIZE=5
```

Load in `app.py`:

```python
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
app.config['DEADLINE'] = datetime.fromisoformat(os.getenv('DEADLINE_TIMESTAMP'))
app.config['MAX_TEAM_SIZE'] = int(os.getenv('MAX_TEAM_SIZE'))
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] Home page loads correctly
- [ ] Navigation works on all pages
- [ ] File upload accepts valid files
- [ ] File upload rejects invalid files
- [ ] Progress bar animates during upload
- [ ] Results page displays correctly
- [ ] Score animation works
- [ ] Category sections expand/collapse
- [ ] Download report works
- [ ] Mobile responsive on all pages
- [ ] All links work correctly

### Browser Testing

Test on:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📱 Mobile Responsiveness

The interface is fully responsive with breakpoints at:
- **Desktop**: 1200px and above
- **Tablet**: 768px - 1199px
- **Mobile**: 576px - 767px
- **Small Mobile**: Below 576px

## ♿ Accessibility Features

- Semantic HTML structure
- ARIA labels for screen readers
- Keyboard navigation support
- Focus indicators
- High contrast mode support
- Reduced motion support
- Alt text for images

## 🐛 Troubleshooting

### Port Already in Use

If port 5000 is already in use, change it in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Flask Not Found

Make sure you've activated the virtual environment:

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Upload Fails

Check that the `uploads/` directory exists and has write permissions.

### Styles Not Loading

Clear your browser cache or do a hard refresh:
- Windows/Linux: `Ctrl + Shift + R`
- Mac: `Cmd + Shift + R`

## 📝 Development Notes

### Mock Data

The application currently generates realistic mock data for demonstration purposes. The mock data includes:
- Pass/fail status for each of the 8 red flags
- Random compliance scores (65-95%)
- Various issue types and severities
- Detailed findings for each validation point
- Actionable recommendations

### File Upload

Files are saved to the `uploads/` directory. For production:
- Implement ZIP file extraction and validation
- Add virus scanning before processing
- Use cloud storage (AWS S3, Azure Blob, etc.)
- Implement automatic file cleanup after validation
- Add file size limits and format validation

### 8 Red Flags Implementation

To implement real validation:

1. **bob_sessions Folder**: Check for folder existence, validate export format, verify timestamps
2. **Exposed Credentials**: Regex patterns for API keys, passwords, tokens; entropy analysis
3. **Banned AI Models**: Check for references to ChatGPT, Claude, Gemini, etc. in code/docs
4. **Team Roster**: Parse team file, validate max 5 members, check for duplicates
5. **Timestamp Validation**: Check file modification times against May 3, 2026 deadline
6. **Video Presence**: Look for video files (.mp4, .mov, .avi) in submission
7. **Deliverables Completeness**: Verify all 4 required components are present
8. **Personal Information**: Scan for PI data patterns, social media scrapes

### Security Considerations

For production deployment:
- Change the `SECRET_KEY` in `app.py`
- Enable HTTPS
- Implement rate limiting to prevent abuse
- Add authentication for judges/organizers
- Validate all inputs thoroughly
- Use environment variables for sensitive data
- Implement proper error handling and logging

## 🚀 Deployment

### Local Development

```bash
python app.py
```

### Production (using Gunicorn)

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t compliance-evaluator .
docker run -p 5000:5000 compliance-evaluator
```

## 📄 License

This project was created for the IBM Bob Dev Day Hackathon May 2026.

### Project License
Copyright (c) 2026 AI Compliance Evaluator Team

Permission is hereby granted to use, copy, modify, and distribute this software
for the purposes of the IBM Bob Dev Day Hackathon May 2026.

### Third-Party Licenses

This project uses the following third-party libraries:

- **Flask** (BSD-3-Clause License) - Copyright 2010 Pallets
- **Werkzeug** (BSD-3-Clause License) - Copyright 2007 Pallets
- **python-dotenv** (BSD-3-Clause License)

See `THIRD-PARTY-LICENSES.txt` for complete license texts.

**Important**: We do not claim ownership of any third-party code. All third-party
libraries retain their original copyrights and licenses.

## 👥 Team

Developed by the AI Compliance Evaluator team for IBM Bob Dev Day Hackathon May 2026.

## 🤝 Contributing

This is a demonstration project for the IBM Bob Dev Day Hackathon May 2026. For questions or issues, please contact the development team.

## 📞 Support

For setup issues or questions:
1. Check `SETUP_INSTRUCTIONS.md` for detailed troubleshooting
2. Review `QUICKSTART.md` for common setup scenarios
3. Ensure Python 3.8+ is properly installed
4. Verify all dependencies are installed correctly

## ⚠️ Important Deadlines

**Submission Deadline:** May 3, 2026, 10:00 AM ET

Use this checker to validate your submission **before** the deadline to ensure compliance with all 8 red flags.

## 🎯 Target Users

- **Hackathon Participants:** Validate your submission before final upload
- **Judges:** Quick compliance verification of submissions
- **Organizers:** Automated pre-screening of entries

## 🎉 Acknowledgments

- Bootstrap team for the excellent CSS framework
- Flask team for the lightweight web framework
- IBM for hosting the Bob Dev Day Hackathon May 2026
- IBM Bob IDE for enabling rapid development

---

**Built with IBM Bob IDE for IBM Bob Dev Day Hackathon May 2026**