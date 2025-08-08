"""
Resume Analyzer Module (Optimized)
Core analysis logic that combines parsing, ATS simulation, and scoring
"""

import re
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from .company_ats import CompanyATS

@dataclass
class AnalysisResult:
    """Dataclass to store analysis results"""
    overall_score: float
    ats_results: Dict
    section_analysis: Dict
    keyword_gaps: Dict
    job_description_analysis: Dict
    recommendations: List[Dict]
    company: str
    resume_summary: Dict

class ResumeAnalyzer:
    def __init__(self):
        self.company_ats = CompanyATS()
        self._setup_keyword_mappings()
        
    def _setup_keyword_mappings(self):
        """Initialize keyword mappings for analysis"""
        self.skill_keywords = [
            'python', 'java', 'javascript', 'c++', 'sql', 'html', 'css',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git',
            'machine learning', 'ai', 'data science', 'analytics'
        ]
        
        self.responsibility_indicators = [
            'responsible for', 'will be responsible', 'responsibilities include',
            'key responsibilities', 'duties include', 'role involves'
        ]
        
        self.education_keywords = ['bachelor', 'master', 'phd', 'degree']
        
    def analyze_resume(self, resume_data: Dict, company: str = "Generic", 
                      job_description: Optional[str] = None, mode: str = "rule") -> AnalysisResult:
        """Perform comprehensive resume analysis with optimized scoring"""
        
        # Validate inputs
        if not isinstance(resume_data, dict):
            raise ValueError("resume_data must be a dictionary")
            
        if company not in self.company_ats.get_available_companies():
            company = "Generic"
            
        if mode not in ["rule", "smart"]:
            mode = "rule"
        
        # Get ATS simulation results
        ats_results = self.company_ats.simulate_ats_filtering(resume_data, company, mode)
        
        # Analyze job description if provided
        jd_analysis = self._analyze_job_description(job_description) if job_description else {}
        
        # Calculate keyword gaps using ATS profile
        keyword_gaps = self._calculate_keyword_gaps(resume_data, jd_analysis, company)
        
        # Section-wise analysis
        section_analysis = self._analyze_sections(resume_data, company)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            resume_data, ats_results, keyword_gaps, section_analysis, company
        )
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(ats_results, section_analysis)
        
        return AnalysisResult(
            overall_score=overall_score,
            ats_results=ats_results,
            section_analysis=section_analysis,
            keyword_gaps=keyword_gaps,
            job_description_analysis=jd_analysis,
            recommendations=recommendations,
            company=company,
            resume_summary=self._generate_resume_summary(resume_data)
        )
    
    def _analyze_job_description(self, job_description: str) -> Dict:
        """Optimized job description analysis using regex patterns"""
        if not job_description:
            return {}
            
        jd_lower = job_description.lower()
        
        # Extract required skills
        found_skills = [skill for skill in self.skill_keywords if skill in jd_lower]
        
        # Extract experience requirements
        exp_pattern = r'(\d+)\+?\s*years?\s*(of\s*)?(experience|exp)'
        exp_matches = re.findall(exp_pattern, jd_lower)
        required_experience = max([int(match[0]) for match in exp_matches]) if exp_matches else 0
        
        # Extract education requirements
        required_education = [edu for edu in self.education_keywords if edu in jd_lower]
        
        # Extract key responsibilities
        responsibilities = []
        for indicator in self.responsibility_indicators:
            if indicator in jd_lower:
                start_idx = jd_lower.find(indicator)
                text_after = job_description[start_idx:start_idx + 500]
                responsibilities.append(text_after.split('.')[0])
        
        return {
            'required_skills': found_skills,
            'required_experience': required_experience,
            'required_education': required_education,
            'key_responsibilities': responsibilities,
            'total_keywords': len(job_description.split())
        }
    
    def _calculate_keyword_gaps(self, resume_data: Dict, jd_analysis: Dict, company: str) -> Dict:
        """Optimized keyword gap analysis using ATS profile"""
        resume_text = resume_data.get('raw_text', '').lower()
        resume_skills = set(skill.lower() for skill in resume_data.get('skills', []))
        
        # Get company profile and keywords
        ats_profile = self.company_ats.get_ats_profile(company)
        company_keywords = set(kw.lower() for kw in ats_profile.preferred_keywords)
        
        # Check for synonyms
        matched_with_synonyms = 0
        for kw in company_keywords:
            if kw in resume_text:
                matched_with_synonyms += 1
            elif kw in self.company_ats.synonym_map:
                if any(syn in resume_text for syn in self.company_ats.synonym_map[kw]):
                    matched_with_synonyms += 0.8
        
        # Job description requirements
        jd_skills = set(skill.lower() for skill in jd_analysis.get('required_skills', []))
        
        # Find gaps and matches
        missing_company_keywords = company_keywords - set(resume_text.split())
        missing_jd_skills = jd_skills - resume_skills
        matched_company_keywords = company_keywords.intersection(set(resume_text.split()))
        matched_jd_skills = jd_skills.intersection(resume_skills)
        
        return {
            'missing_company_keywords': list(missing_company_keywords),
            'missing_jd_skills': list(missing_jd_skills),
            'matched_company_keywords': list(matched_company_keywords),
            'matched_jd_skills': list(matched_jd_skills),
            'keyword_match_percentage': (matched_with_synonyms / len(company_keywords) * 100 
                                       if company_keywords else 0),
            'jd_skill_match_percentage': (len(matched_jd_skills) / len(jd_skills) * 100 
                                       if jd_skills else 0)
        }
    
    def _analyze_sections(self, resume_data: Dict, company: str) -> Dict:
        """Optimized section analysis with ATS profile awareness"""
        sections = resume_data.get('sections', {})
        analysis = {}
        ats_profile = self.company_ats.get_ats_profile(company)
        
        # Analyze each section
        for section_name, content in sections.items():
            strength = self._assess_section_strength(section_name, content, company)
            
            analysis[section_name] = {
                'present': True,
                'word_count': len(content.split()),
                'strength': strength,
                'suggestions': self._get_section_suggestions(
                    section_name, content, company, strength, ats_profile
                )
            }
        
        # Check for missing critical sections
        critical_sections = ['experience', 'education', 'skills']
        if ats_profile.company in ['Google', 'Amazon', 'Microsoft']:
            critical_sections.append('summary')
            
        for critical in critical_sections:
            if critical not in analysis:
                analysis[critical] = {
                    'present': False,
                    'word_count': 0,
                    'strength': 'Poor',
                    'suggestions': [f'Add a {critical} section to your resume']
                }
        
        return analysis
    
    def _assess_section_strength(self, section_name: str, content: str, company: str) -> str:
        """Optimized section strength assessment with company awareness"""
        word_count = len(content.split())
        content_lower = content.lower()
        ats_profile = self.company_ats.get_ats_profile(company)
        
        if section_name == 'experience':
            if word_count > 200 and any(kw in content_lower 
                                      for kw in ['achieved', 'led', 'managed']):
                return 'Excellent'
            return 'Good' if word_count > 100 else 'Fair' if word_count > 50 else 'Poor'
        
        elif section_name == 'skills':
            skill_count = len([word for word in content.split() if len(word) > 2])
            threshold = 15 if ats_profile.company in ['Google', 'Amazon'] else 10
            if skill_count > threshold:
                return 'Excellent'
            return 'Good' if skill_count > threshold-5 else 'Fair' if skill_count > 5 else 'Poor'
        
        elif section_name == 'summary':
            if 50 < word_count < 150:
                return 'Good'
            return 'Fair' if word_count > 20 else 'Poor'
        
        return 'Good' if word_count > 50 else 'Fair' if word_count > 20 else 'Poor'
    
    def _get_section_suggestions(self, section_name: str, content: str, 
                               company: str, strength: str, ats_profile: ATSProfile) -> List[str]:
        """Optimized section suggestions with company-specific advice"""
        suggestions = []
        content_lower = content.lower()
        
        if section_name == 'experience' and strength in ['Fair', 'Poor']:
            if 'achieved' not in content_lower:
                suggestions.append('Add quantifiable achievements and metrics')
            if not any(kw in content_lower for kw in ['led', 'managed', 'directed']):
                suggestions.append('Include leadership and management experience')
        
        elif section_name == 'skills':
            missing_skills = [skill for skill in ats_profile.preferred_keywords 
                            if skill.lower() not in content_lower]
            if missing_skills:
                suggestions.append(f'Consider adding: {", ".join(list(missing_skills)[:3])}')
        
        elif section_name == 'summary' and strength in ['Fair', 'Poor']:
            suggestions.append('Expand summary to 3-4 sentences highlighting key strengths')
        
        return suggestions
    
    def _generate_recommendations(self, resume_data: Dict, ats_results: Dict, 
                                keyword_gaps: Dict, section_analysis: Dict, company: str) -> List[Dict]:
        """Optimized recommendation generation with priority scoring"""
        recommendations = []
        ats_profile = self.company_ats.get_ats_profile(company)
        
        # Priority scoring system (1-3, higher is more important)
        priorities = []
        
        # ATS-based recommendations
        if ats_results['overall_ats_score'] < 70:
            priorities.append({
                'score': 3,
                'category': 'ATS Optimization',
                'title': 'Improve ATS Compatibility',
                'description': 'Your resume needs optimization for ATS systems',
                'actions': [
                    'Add more relevant keywords',
                    'Improve formatting and structure',
                    'Include required skills'
                ]
            })
        
        # Keyword gap recommendations
        if keyword_gaps['missing_company_keywords']:
            priorities.append({
                'score': 3 if len(keyword_gaps['missing_company_keywords']) > 5 else 2,
                'category': 'Keywords',
                'title': 'Add Company-Specific Keywords',
                'description': f'Missing important keywords for {company}',
                'actions': [
                    f'Include: {", ".join(list(keyword_gaps["missing_company_keywords"])[:3])}'
                ]
            })
        
        # Section improvement recommendations
        weak_sections = [name for name, data in section_analysis.items() 
                        if data['strength'] in ['Poor', 'Fair']]
        
        if weak_sections:
            priorities.append({
                'score': 2,
                'category': 'Content',
                'title': 'Strengthen Weak Sections',
                'description': 'Some sections need improvement',
                'actions': [f'Improve {section} section' for section in weak_sections[:2]]
            })
        
        # Experience recommendations
        years_exp = resume_data.get('experience_years', 0)
        req_exp = ats_profile.experience_requirements.get('mid', 3)
        if years_exp < req_exp:
            priorities.append({
                'score': 2 if (req_exp - years_exp) > 2 else 1,
                'category': 'Experience',
                'title': 'Highlight All Relevant Experience',
                'description': 'Include internships, projects, and freelance work',
                'actions': [
                    'Add internship experience',
                    'Include significant projects',
                    'Mention freelance or volunteer work'
                ]
            })
        
        # Format recommendations
        if ats_results['format_score'] < 80:
            priorities.append({
                'score': 1,
                'category': 'Format',
                'title': 'Improve Resume Format',
                'description': 'Format optimization for better ATS parsing',
                'actions': [
                    'Use standard section headings',
                    'Ensure contact information is clear',
                    'Use bullet points for better readability'
                ]
            })
        
        # Sort by priority score (highest first)
        priorities.sort(key=lambda x: x['score'], reverse=True)
        
        # Convert to final recommendation format
        for item in priorities:
            recommendations.append({
                'priority': 'High' if item['score'] == 3 else 'Medium' if item['score'] == 2 else 'Low',
                'category': item['category'],
                'title': item['title'],
                'description': item['description'],
                'action_items': item['actions']
            })
        
        return recommendations
    
    def _calculate_overall_score(self, ats_results: Dict, section_analysis: Dict) -> int:
        """Optimized scoring calculation with ATS profile awareness"""
        ats_score = ats_results['overall_ats_score']
        
        # Section quality score
        section_scores = {
            'Excellent': 100,
            'Good': 80,
            'Fair': 60,
            'Poor': 40
        }
        
        present_sections = [data for data in section_analysis.values() if data['present']]
        avg_section_score = (sum(section_scores.get(data['strength'], 40) 
                           for data in present_sections) / len(present_sections)) if present_sections else 40
        
        # Weighted average favoring ATS score
        return int(min((ats_score * 0.7) + (avg_section_score * 0.3), 100))
    
    def _generate_resume_summary(self, resume_data: Dict) -> Dict:
        """Optimized resume summary generation"""
        return {
            'total_experience': resume_data.get('experience_years', 0),
            'education_level': resume_data.get('education_level', 'Unknown'),
            'skill_count': len(resume_data.get('skills', [])),
            'has_contact_info': bool(resume_data.get('contact_info', {}).get('email')),
            'section_count': len(resume_data.get('sections', {})),
            'word_count': len(resume_data.get('raw_text', '').split()),
            'last_updated': resume_data.get('last_updated', 'Unknown')
        }