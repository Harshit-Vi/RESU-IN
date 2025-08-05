"""
Resume Analyzer Module
Core analysis logic that combines parsing, ATS simulation, and scoring
"""

import re
from typing import Dict, List, Optional
from .company_ats import CompanyATS

class ResumeAnalyzer:
    def __init__(self):
        self.company_ats = CompanyATS()
        
    def analyze_resume(self, resume_data: Dict, company: str, job_description: Optional[str] = None) -> Dict:
        """Perform comprehensive resume analysis"""
        
        # Get ATS simulation results
        ats_results = self.company_ats.simulate_ats_filtering(resume_data, company)
        
        # Analyze job description if provided
        jd_analysis = self._analyze_job_description(job_description) if job_description else {}
        
        # Calculate keyword gaps
        keyword_gaps = self._calculate_keyword_gaps(resume_data, jd_analysis, company)
        
        # Section-wise analysis
        section_analysis = self._analyze_sections(resume_data, company)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            resume_data, ats_results, keyword_gaps, section_analysis, company
        )
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(ats_results, section_analysis)
        
        return {
            'overall_score': overall_score,
            'ats_results': ats_results,
            'section_analysis': section_analysis,
            'keyword_gaps': keyword_gaps,
            'job_description_analysis': jd_analysis,
            'recommendations': recommendations,
            'company': company,
            'resume_summary': self._generate_resume_summary(resume_data)
        }
    
    def _analyze_job_description(self, job_description: str) -> Dict:
        """Analyze job description to extract requirements"""
        jd_lower = job_description.lower()
        
        # Extract required skills
        skill_keywords = [
            'python', 'java', 'javascript', 'c++', 'sql', 'html', 'css',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git',
            'machine learning', 'ai', 'data science', 'analytics'
        ]
        
        found_skills = [skill for skill in skill_keywords if skill in jd_lower]
        
        # Extract experience requirements
        exp_pattern = r'(\d+)\+?\s*years?\s*(of\s*)?(experience|exp)'
        exp_matches = re.findall(exp_pattern, jd_lower)
        required_experience = 0
        if exp_matches:
            required_experience = max([int(match[0]) for match in exp_matches])
        
        # Extract education requirements
        education_keywords = ['bachelor', 'master', 'phd', 'degree']
        required_education = [edu for edu in education_keywords if edu in jd_lower]
        
        # Extract key responsibilities
        responsibility_indicators = [
            'responsible for', 'will be responsible', 'responsibilities include',
            'key responsibilities', 'duties include', 'role involves'
        ]
        
        responsibilities = []
        for indicator in responsibility_indicators:
            if indicator in jd_lower:
                # Extract text after the indicator
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
        """Calculate gaps between resume and job requirements"""
        resume_text = resume_data.get('raw_text', '').lower()
        resume_skills = set(skill.lower() for skill in resume_data.get('skills', []))
        
        # Get company preferred keywords
        ats_profile = self.company_ats.get_ats_profile(company)
        company_keywords = set(keyword.lower() for keyword in ats_profile.preferred_keywords)
        
        # Job description requirements
        jd_skills = set(skill.lower() for skill in jd_analysis.get('required_skills', []))
        
        # Find gaps
        missing_company_keywords = company_keywords - set(resume_text.split())
        missing_jd_skills = jd_skills - resume_skills
        
        # Find matches
        matched_company_keywords = company_keywords.intersection(set(resume_text.split()))
        matched_jd_skills = jd_skills.intersection(resume_skills)
        
        return {
            'missing_company_keywords': list(missing_company_keywords),
            'missing_jd_skills': list(missing_jd_skills),
            'matched_company_keywords': list(matched_company_keywords),
            'matched_jd_skills': list(matched_jd_skills),
            'keyword_match_percentage': len(matched_company_keywords) / len(company_keywords) * 100 if company_keywords else 0,
            'jd_skill_match_percentage': len(matched_jd_skills) / len(jd_skills) * 100 if jd_skills else 0
        }
    
    def _analyze_sections(self, resume_data: Dict, company: str) -> Dict:
        """Analyze individual resume sections"""
        sections = resume_data.get('sections', {})
        analysis = {}
        
        # Analyze each section
        for section_name, content in sections.items():
            analysis[section_name] = {
                'present': True,
                'word_count': len(content.split()),
                'strength': self._assess_section_strength(section_name, content, company),
                'suggestions': self._get_section_suggestions(section_name, content, company)
            }
        
        # Check for missing critical sections
        critical_sections = ['experience', 'education', 'skills', 'summary']
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
        """Assess the strength of a resume section"""
        word_count = len(content.split())
        
        if section_name == 'experience':
            if word_count > 200 and 'achieved' in content.lower():
                return 'Excellent'
            elif word_count > 100:
                return 'Good'
            elif word_count > 50:
                return 'Fair'
            else:
                return 'Poor'
        
        elif section_name == 'skills':
            skill_count = len([word for word in content.split() if len(word) > 2])
            if skill_count > 15:
                return 'Excellent'
            elif skill_count > 10:
                return 'Good'
            elif skill_count > 5:
                return 'Fair'
            else:
                return 'Poor'
        
        elif section_name == 'summary':
            if word_count > 50 and word_count < 150:
                return 'Good'
            elif word_count > 20:
                return 'Fair'
            else:
                return 'Poor'
        
        else:
            if word_count > 50:
                return 'Good'
            elif word_count > 20:
                return 'Fair'
            else:
                return 'Poor'
    
    def _get_section_suggestions(self, section_name: str, content: str, company: str) -> List[str]:
        """Get suggestions for improving a section"""
        suggestions = []
        
        if section_name == 'experience':
            if 'achieved' not in content.lower():
                suggestions.append('Add quantifiable achievements and metrics')
            if 'led' not in content.lower() and 'managed' not in content.lower():
                suggestions.append('Include leadership and management experience')
        
        elif section_name == 'skills':
            ats_profile = self.company_ats.get_ats_profile(company)
            content_lower = content.lower()
            missing_skills = [skill for skill in ats_profile.preferred_keywords 
                            if skill not in content_lower]
            if missing_skills:
                suggestions.append(f'Consider adding: {", ".join(list(missing_skills)[:5])}')
        
        elif section_name == 'summary':
            if len(content.split()) < 30:
                suggestions.append('Expand summary to 3-4 sentences highlighting key strengths')
        
        return suggestions
    
    def _generate_recommendations(self, resume_data: Dict, ats_results: Dict, 
                                keyword_gaps: Dict, section_analysis: Dict, company: str) -> List[Dict]:
        """Generate prioritized recommendations"""
        recommendations = []
        
        # ATS-based recommendations
        if ats_results['overall_ats_score'] < 70:
            recommendations.append({
                'priority': 'High',
                'category': 'ATS Optimization',
                'title': 'Improve ATS Compatibility',
                'description': 'Your resume needs optimization for ATS systems',
                'action_items': [
                    'Add more relevant keywords',
                    'Improve formatting and structure',
                    'Include required skills'
                ]
            })
        
        # Keyword gap recommendations
        if keyword_gaps['missing_company_keywords']:
            recommendations.append({
                'priority': 'High',
                'category': 'Keywords',
                'title': 'Add Company-Specific Keywords',
                'description': f'Missing important keywords for {company}',
                'action_items': [
                    f'Include: {", ".join(list(keyword_gaps["missing_company_keywords"])[:5])}'
                ]
            })
        
        # Section improvement recommendations
        weak_sections = [name for name, data in section_analysis.items() 
                        if data['strength'] in ['Poor', 'Fair']]
        
        if weak_sections:
            recommendations.append({
                'priority': 'Medium',
                'category': 'Content',
                'title': 'Strengthen Weak Sections',
                'description': 'Some sections need improvement',
                'action_items': [f'Improve {section} section' for section in weak_sections[:3]]
            })
        
        # Experience recommendations
        years_exp = resume_data.get('experience_years', 0)
        ats_profile = self.company_ats.get_ats_profile(company)
        if years_exp < ats_profile.experience_requirements.get('mid', 3):
            recommendations.append({
                'priority': 'Medium',
                'category': 'Experience',
                'title': 'Highlight All Relevant Experience',
                'description': 'Include internships, projects, and freelance work',
                'action_items': [
                    'Add internship experience',
                    'Include significant projects',
                    'Mention freelance or volunteer work'
                ]
            })
        
        # Format recommendations
        if ats_results['format_score'] < 80:
            recommendations.append({
                'priority': 'Low',
                'category': 'Format',
                'title': 'Improve Resume Format',
                'description': 'Format optimization for better ATS parsing',
                'action_items': [
                    'Use standard section headings',
                    'Ensure contact information is clear',
                    'Use bullet points for better readability'
                ]
            })
        
        return recommendations
    
    def _calculate_overall_score(self, ats_results: Dict, section_analysis: Dict) -> int:
        """Calculate overall resume score"""
        # Base score from ATS
        ats_score = ats_results['overall_ats_score']
        
        # Section quality score
        section_scores = {
            'Excellent': 100,
            'Good': 80,
            'Fair': 60,
            'Poor': 40
        }
        
        present_sections = [data for data in section_analysis.values() if data['present']]
        if present_sections:
            avg_section_score = sum([section_scores.get(data['strength'], 40) 
                                   for data in present_sections]) / len(present_sections)
        else:
            avg_section_score = 40
        
        # Weighted average
        overall_score = (ats_score * 0.6) + (avg_section_score * 0.4)
        
        return int(min(overall_score, 100))
    
    def _generate_resume_summary(self, resume_data: Dict) -> Dict:
        """Generate a summary of the resume"""
        return {
            'total_experience': resume_data.get('experience_years', 0),
            'education_level': resume_data.get('education_level', 'Unknown'),
            'skill_count': len(resume_data.get('skills', [])),
            'has_contact_info': bool(resume_data.get('contact_info', {}).get('email')),
            'section_count': len(resume_data.get('sections', {})),
            'word_count': len(resume_data.get('raw_text', '').split())
        }