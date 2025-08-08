"""
Resume Parser Module
Extracts and processes resume data from PDF/DOCX files, with OCR fallback.
"""

import re
import os
import csv
from typing import Dict, List, Optional

try:
    import PyPDF2
    import docx
    from pdf2image import convert_from_path
    import pytesseract
    from PIL import Image
except ImportError as e:
    raise ImportError(
        "Required packages not installed. Run: pip install PyPDF2 python-docx pytesseract pdf2image pillow"
    ) from e


class ResumeParser:
    def __init__(self):
        self.skills_list = self._load_skills()

    def parse_resume(self, file_path: str) -> Optional[Dict]:
        """Main entry point: parse a resume file and return structured data."""
        text = self._extract_text(file_path)
        if not text:
            print("❌ Unable to extract text from resume.")
            return None

        resume_data = self._parse_resume_text(text)
        return resume_data

    def _extract_text(self, file_path: str) -> str:
        """Extract raw text from PDF or DOCX, with OCR fallback."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            text = self._extract_pdf_text(file_path)
        elif ext in (".docx", ".doc"):
            text = self._extract_docx_text(file_path)
        else:
            raise ValueError("Unsupported file format")

        if not text.strip():
            # Fallback to OCR if text extraction failed
            text = self._ocr_pdf(file_path) if ext == ".pdf" else ""
        return text

    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF using PyPDF2."""
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX using python-docx."""
        doc = docx.Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs)

    def _ocr_pdf(self, file_path: str) -> str:
        """Perform OCR on each page of the PDF."""
        text = ""
        images = convert_from_path(file_path)
        for img in images:
            text += pytesseract.image_to_string(img)
        return text

    def _parse_resume_text(self, text: str) -> Dict:
        """Parse extracted text into structured resume data."""
        return {
            "contact_info": self._extract_contact_info(text),
            "skills": self._extract_skills(text),
            "experience_years": self._estimate_experience(text),
            "sections": self._detect_sections(text),
        }

    def _extract_contact_info(self, text: str) -> Dict:
        """Extract phone, email, LinkedIn, etc."""
        email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        phone = re.findall(r"\+?\d[\d\s-]{7,}\d", text)
        linkedin = re.findall(r"https?://(www\.)?linkedin\.com/[A-Za-z0-9\-/]+", text)
        return {
            "emails": email,
            "phones": phone,
            "linkedin": linkedin
        }

    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text based on a predefined list."""
        found_skills = []
        text_lower = text.lower()
        for skill in self.skills_list:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        return list(set(found_skills))

    def _estimate_experience(self, text: str) -> int:
        """Estimate years of experience from date ranges."""
        years = re.findall(r"(20\d{2}|19\d{2})", text)
        if years:
            years = sorted(set(map(int, years)))
            return max(0, max(years) - min(years))
        return 0

    def _detect_sections(self, text: str) -> Dict[str, str]:
        """Detect common resume sections."""
        sections = {
            "experience": "",
            "education": "",
            "skills": "",
            "projects": "",
            "certifications": "",
        }
        # This is a naive section detection — can be improved with NLP
        lines = text.splitlines()
        current_section = None
        for line in lines:
            line_clean = line.strip().lower()
            for section in sections.keys():
                if section in line_clean:
                    current_section = section
                    break
            else:
                if current_section:
                    sections[current_section] += line + "\n"
        return sections

    def _load_skills(self) -> List[str]:
        """Load skills from CSV file or use default list."""
        skills_file = os.path.join(os.path.dirname(__file__), "data", "skills.csv")
        if os.path.exists(skills_file):
            with open(skills_file, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                return [row[0] for row in reader if row]
        else:
            return ["Python", "Java", "C++", "SQL", "JavaScript", "HTML", "CSS"]


if __name__ == "__main__":
    parser = ResumeParser()
    test_path = input("Enter path to resume: ").strip()
    result = parser.parse_resume(test_path)
    if result:
        print(result)
