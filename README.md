# Welcome to our RESU-IN Project

A Python-based, company-specific Resume Analysis Tool that simulates Applicant Tracking System (ATS) behavior and provides actionable improvement recommendations.

## 📌 About
RESU-IN parses resumes, evaluates them against target companies' ATS profiles, and generates detailed analysis reports. It supports multiple ATS simulation modes and provides keyword matching, section analysis, and job description alignment.

## ✨ Features
- Multi-company ATS simulation – Amazon, Google, Microsoft, Generic profiles (easily extendable)
- Two analysis modes: Rule-based (deterministic) and Smart mode (flexible matching)
- Resume parsing from PDF/DOCX – Extracts sections, keywords, experience, education
- Company-specific keyword analysis – Highlights matched and missing terms
- Job description matching – Measures overlap between JD and resume
- Detailed report generation – ATS results, section analysis, keyword coverage, recommendations
- CLI interface – Interactive prompts for resume, company, and job description

## 🗂 Project Structure
```
RESU-IN/
├── main.py                  # Entry point for the application
├── modules/
│   ├── __init__.py           # Module initializer
│   ├── resume_parser.py      # Extracts data from resumes
│   ├── company_ats.py        # Company ATS profiles & simulation logic
│   ├── analyzer.py           # Combines parsing + ATS scoring
│   ├── report_generator.py   # Generates formatted analysis reports
└── README.md                 # Project documentation
```

## ⚙️ Installation
1. Clone the repository:
```bash
git clone https://github.com/<your-username>/RESU-IN.git
cd RESU-IN
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage
Run the application:
```bash
python main.py
```
Follow prompts for resume path, company selection, job description, and mode.

## 🖥 Example Output
```
🎯 RESUIN - Advanced Resume Analyzer
Analyzes resumes against company-specific ATS systems
Provides detailed scoring and improvement recommendations

📄 Enter resume file path (PDF/DOCX): resume.pdf
✅ Resume file loaded: resume.pdf

🏢 Select target company:
1. Amazon
2. Google
3. Microsoft
4. Generic
```

## 🏗 Extending the Project
- Add new companies in `_initialize_ats_profiles()` in `company_ats.py`
- Enhance `resume_parser.py` to handle more formats or richer extraction
- Implement ML scoring in smart mode for advanced evaluation

## 📄 License
MIT License

## 🤝 Contributing
Pull requests and suggestions are welcome. Open an issue or submit a PR for bugs or features.

## 🛠 Editing and Pushing Updates
1. **Directly in GitHub Web UI**:
   - Navigate to your repository on GitHub.
   - Open `README.md` and click the edit (pencil) icon.
   - Make your changes, add a commit message, and click **Commit changes**.

2. **Using a Local Text Editor**:
   - Open the repository folder on your computer.
   - Edit `README.md` using VS Code, Sublime Text, or any text editor.
   - Save changes and commit with:
     ```bash
     git add README.md
     git commit -m "Updated README"
     git push origin main
     ```

3. **Using GitHub Desktop**:
   - Open your repository in GitHub Desktop.
   - Edit `README.md` in your preferred editor.
   - Commit and push changes via the GitHub Desktop interface.

## 👨‍💻 Author
Developed by Harshit Singh


