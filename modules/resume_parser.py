"""
Resume Parser Module
Handles parsing of PDF and DOCX resume files
"""

import os
import re
import pytesseract
from typing import Dict, List, Optional
from pdf2image import convert_from_path
try:
    import PyPDF2
    from docx import Document
except ImportError:
    print("Required packages not installed. Please install:")
    print("pip install PyPDF2 python-docx")
    exit(1)

class ResumeParser:
    def __init__(self):
        self.sections = {
            'contact': ['contact', 'personal', 'details'],
            'summary': ['summary', 'objective', 'profile', 'about'],
            'experience': ['experience', 'work', 'employment', 'career'],
            'education': ['education', 'academic', 'qualification'],
            'skills': ['skills', 'technical', 'competencies', 'expertise'],
            'projects': ['projects', 'portfolio', 'work samples'],
            'certifications': ['certifications', 'certificates', 'licenses'],
            'achievements': ['achievements', 'awards', 'honors', 'accomplishments']
        }
        
    def parse_resume(self, file_path: str) -> Optional[Dict]:
        """Parse resume file and extract structured data"""
        try:
            if file_path.lower().endswith('.pdf'):
                text = self._extract_pdf_text(file_path)
            elif file_path.lower().endswith(('.docx', '.doc')):
                text = self._extract_docx_text(file_path)
            else:
                raise ValueError("Unsupported file format")
                
            if not text:
                return None
                
            return self._parse_resume_text(text)
            
        except Exception as e:
            print(f"Error parsing resume: {str(e)}")
            return None
    
    
def _extract_pdf_text(self, file_path: str) -> str:
    """Extract text from PDF file, with OCR fallback"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
                else:
                    # OCR fallback
                    images = convert_from_path(file_path)
                    for img in images:
                        text += pytesseract.image_to_string(img)
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
    return text
    
    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX: {str(e)}")
        return text
    
    def _parse_resume_text(self, text: str) -> Dict:
        """Parse resume text into structured data"""
        resume_data = {
            'raw_text': text,
            'sections': {},
            'contact_info': self._extract_contact_info(text),
            'skills': self._extract_skills(text),
            'experience_years': self._calculate_experience_years(text),
            'keywords': self._extract_keywords(text),
            'education_level': self._extract_education_level(text)
        }
        
        # Parse sections
        lines = text.split('\n')
        current_section = 'general'
        section_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line is a section header
            section_key = self._identify_section(line)
            if section_key:
                # Save previous section
                if section_content:
                    resume_data['sections'][current_section] = '\n'.join(section_content)
                # Start new section
                current_section = section_key
                section_content = []
            else:
                section_content.append(line)
        
        # Save last section
        if section_content:
            resume_data['sections'][current_section] = '\n'.join(section_content)
            
        return resume_data
    
    def _identify_section(self, line: str) -> Optional[str]:
        """Identify if a line is a section header"""
        line_lower = line.lower().strip()
        
        for section, keywords in self.sections.items():
            for keyword in keywords:
                if keyword in line_lower and len(line.split()) <= 3:
                    return section
        return None
    
    def _extract_contact_info(self, text: str) -> Dict:
        """Extract contact information"""
        contact_info = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]
        
        # Phone
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info['phone'] = ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
        
        # LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin:
            contact_info['linkedin'] = linkedin.group()
            
        return contact_info
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        # Common technical skills (can be expanded)
        common_skills = [
            'python', 'java', 'javascript', 'c++', 'c#', 'sql', 'html', 'css',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'jenkins',
            'tensorflow', 'pytorch', 'machine learning', 'data science',
            'project management', 'agile', 'scrum', 'leadership', 'communication'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in common_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
                
        return found_skills
    
    def _calculate_experience_years(self, text: str) -> int:
        """Calculate years of experience from resume"""
        # Look for experience patterns
        exp_patterns = [
            r'(\d+)\+?\s*years?\s*(of\s*)?experience',
            r'experience\s*:?\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*year[s]?\s*(experience|exp)',
        ]
        
        years = 0
        for pattern in exp_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Get the highest number found
                for match in matches:
                    try:
                        year_val = int(match[0] if isinstance(match, tuple) else match)
                        years = max(years, year_val)
                    except (ValueError, IndexError):
                        continue
                        
        return years
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from resume"""
        # Remove common stop words and extract meaningful terms
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be',
            'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would'
        }
        
        # Split text into words and filter
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        keywords = [word for word in words if word not in stop_words]
        
        # Count frequency and return top keywords
        from collections import Counter
        word_freq = Counter(keywords)
        return [word for word, count in word_freq.most_common(50)]
    
    def _extract_education_level(self, text: str) -> str:
        """Extract highest education level"""
        education_levels = {
            'phd': ['phd', 'ph.d', 'doctorate', 'doctoral'],
            'masters': ['masters', 'master\'s', 'm.s', 'mba', 'ma', 'ms'],
            'bachelors': ['bachelors', 'bachelor\'s', 'b.s', 'ba', 'bs', 'b.tech', 'be'],
            'associate': ['associate', 'diploma'],
            'high_school': ['high school', 'secondary', '12th', 'intermediate']
        }
        
        text_lower = text.lower()
        
        for level, keywords in education_levels.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return level
                    
        return 'unknown'