"""
Company ATS Simulation Module
Supports:
1. Original Rule-based scoring
2. Smart ML-simulated scoring (synonym-aware, section-weighted, company-specific quirks)
"""

from typing import Dict, List, Set
from dataclasses import dataclass
import re

@dataclass
class ATSProfile:
    company: str
    keyword_weight: float
    experience_weight: float
    education_weight: float
    skills_weight: float
    format_weight: float
    preferred_keywords: Set[str]
    required_skills: Set[str]
    experience_requirements: Dict[str, int]
    education_preferences: List[str]
    scoring_strictness: float
    common_filters: List[str]

class CompanyATS:
    def __init__(self):
        self.ats_profiles = self._initialize_ats_profiles()
        self.keyword_synonyms = {
            "ml": "machine learning",
            "js": "javascript",
            "gcp": "google cloud platform",
            "aws": "amazon web services",
            "ai": "artificial intelligence",
            "reactjs": "react",
            "node": "node.js"
        }

    def get_available_companies(self) -> List[str]:
        return list(self.ats_profiles.keys())
    
    def get_ats_profile(self, company: str) -> ATSProfile:
        return self.ats_profiles.get(company, self.ats_profiles['Generic'])

    def simulate_ats_filtering(self, resume_data: Dict, company: str) -> Dict:
        print("\nChoose ATS scoring mode:")
        print("1 - Rule-based scoring (original)")
        print("2 - Smart scoring (ML-simulated)")
        mode = input("Enter 1 or 2: ").strip()

        if mode == "2":
            return self._smart_scoring(resume_data, company)
        else:
            return self._rule_based_scoring(resume_data, company)

    # ---------------- RULE-BASED SCORING ----------------
    def _rule_based_scoring(self, resume_data: Dict, company: str) -> Dict:
        profile = self.get_ats_profile(company)
        passes_initial = self._initial_screening(resume_data, profile)
        keyword_score = self._calculate_keyword_score(resume_data, profile)
        experience_score = self._evaluate_experience(resume_data, profile)
        education_score = self._assess_education(resume_data, profile)
        skills_score = self._match_skills(resume_data, profile)
        format_score = self._evaluate_format(resume_data, profile)

        overall_score = (
            keyword_score * profile.keyword_weight +
            experience_score * profile.experience_weight +
            education_score * profile.education_weight +
            skills_score * profile.skills_weight +
            format_score * profile.format_weight
        )

        adjusted_score = overall_score * (1 - profile.scoring_strictness * 0.2)

        return {
            'passes_initial_screening': passes_initial,
            'keyword_score': keyword_score,
            'experience_score': experience_score,
            'education_score': education_score,
            'skills_score': skills_score,
            'format_score': format_score,
            'overall_ats_score': min(adjusted_score, 100),
            'ats_recommendation': self._get_ats_recommendation(adjusted_score),
            'company_specific_notes': self._get_company_notes(resume_data, profile)
        }

    # ---------------- SMART SCORING ----------------
    def _smart_scoring(self, resume_data: Dict, company: str) -> Dict:
        profile = self.get_ats_profile(company)
        expanded_keywords = set(profile.preferred_keywords)
        for kw in list(expanded_keywords):
            if kw.lower() in self.keyword_synonyms:
                expanded_keywords.add(self.keyword_synonyms[kw.lower()])

        section_scores = []
        sections = resume_data.get("sections", {})
        for section_name, content in sections.items():
            weight = 1.5 if section_name in ["experience", "skills"] else 1.0
            matches = sum(1 for kw in expanded_keywords if kw.lower() in content.lower())
            if expanded_keywords:
                section_scores.append((matches / len(expanded_keywords)) * 100 * weight)
        keyword_score = sum(section_scores) / max(len(section_scores), 1)

        resume_skills = set(s.lower() for s in resume_data.get("skills", []))
        for s in list(resume_skills):
            if s in self.keyword_synonyms:
                resume_skills.add(self.keyword_synonyms[s])
        required_skills = set(s.lower() for s in profile.required_skills)
        skill_score = (len(resume_skills & required_skills) / len(required_skills)) * 100 if required_skills else 0

        exp_years = resume_data.get("experience_years", 0)
        exp_score = min(100, (exp_years / profile.experience_requirements.get("senior", 5)) * 100)
        if exp_years >= profile.experience_requirements.get("senior", 5):
            exp_score += 5

        edu_level = resume_data.get("education_level", "unknown")
        if edu_level in profile.education_preferences:
            edu_score = 100 - (profile.education_preferences.index(edu_level) * 20)
        else:
            edu_score = 50

        fmt_score = 100
        for section in ["experience", "education", "skills"]:
            if section not in sections:
                fmt_score -= 15
        if not resume_data.get("contact_info", {}).get("email"):
            fmt_score -= 25

        overall_score = (
            keyword_score * 0.4 +
            skill_score * 0.25 +
            exp_score * 0.2 +
            edu_score * 0.1 +
            fmt_score * 0.05
        )

        if profile.company == "Google" and keyword_score > 90:
            overall_score -= 5
        elif profile.company == "Amazon" and "leadership" in resume_data.get("keywords", []):
            overall_score += 3
        elif profile.company in ["TCS", "Infosys", "Wipro"]:
            overall_score += (skill_score * 0.05)

        passes_initial = overall_score >= (profile.scoring_strictness * 100 * 0.6)

        return {
            'passes_initial_screening': passes_initial,
            'keyword_score': round(keyword_score, 2),
            'experience_score': round(exp_score, 2),
            'education_score': round(edu_score, 2),
            'skills_score': round(skill_score, 2),
            'format_score': round(fmt_score, 2),
            'overall_ats_score': round(min(overall_score, 100), 2),
            'ats_recommendation': self._get_ats_recommendation(overall_score),
            'company_specific_notes': self._get_company_notes(resume_data, profile)
        }

    # ---------------- COMMON METHODS ----------------
    def _initial_screening(self, resume_data: Dict, profile: ATSProfile) -> bool:
        has_contact = bool(resume_data.get('contact_info', {}).get('email'))
        has_content = len(resume_data.get('raw_text', '')) > 100
        has_skills = len(resume_data.get('skills', [])) > 0
        return has_contact and has_content and has_skills

    def _calculate_keyword_score(self, resume_data: Dict, profile: ATSProfile) -> float:
        resume_text = resume_data.get('raw_text', '').lower()
        resume_keywords = set(resume_data.get('keywords', []))
        matched_keywords = sum(1 for kw in profile.preferred_keywords if kw.lower() in resume_text or kw.lower() in resume_keywords)
        return (matched_keywords / len(profile.preferred_keywords) * 100) if profile.preferred_keywords else 0

    def _evaluate_experience(self, resume_data: Dict, profile: ATSProfile) -> float:
        years_experience = resume_data.get('experience_years', 0)
        if years_experience >= profile.experience_requirements.get('senior', 5):
            return 100
        elif years_experience >= profile.experience_requirements.get('mid', 3):
            return 80
        elif years_experience >= profile.experience_requirements.get('entry', 0):
            return 60
        else:
            return 40

    def _assess_education(self, resume_data: Dict, profile: ATSProfile) -> float:
        education_level = resume_data.get('education_level', 'unknown')
        if education_level in profile.education_preferences:
            index = profile.education_preferences.index(education_level)
            return 100 - (index * 20)
        return 50

    def _match_skills(self, resume_data: Dict, profile: ATSProfile) -> float:
        resume_skills = set(skill.lower() for skill in resume_data.get('skills', []))
        required_skills = set(skill.lower() for skill in profile.required_skills)
        matched_skills = len(resume_skills & required_skills)
        return (matched_skills / len(required_skills) * 100) if required_skills else 0

    def _evaluate_format(self, resume_data: Dict, profile: ATSProfile) -> float:
        score = 100
        for section in ['experience', 'education', 'skills']:
            if section not in resume_data.get('sections', {}):
                score -= 20
        if not resume_data.get('contact_info', {}).get('email'):
            score -= 30
        return max(score, 0)

    def _get_ats_recommendation(self, score: float) -> str:
        if score >= 80:
            return "High likelihood of passing ATS screening"
        elif score >= 60:
            return "Moderate likelihood of passing ATS screening"
        elif score >= 40:
            return "Low likelihood of passing ATS screening"
        else:
            return "Very low likelihood of passing ATS screening"

    def _get_company_notes(self, resume_data: Dict, profile: ATSProfile) -> List[str]:
        notes = []
        if profile.company == 'Amazon':
            notes.append("Emphasize leadership principles and customer impact")
            notes.append("Include metrics and scale of systems worked on")
        elif profile.company == 'Google':
            notes.append("Highlight algorithmic thinking and innovation")
            notes.append("Include research publications if any")
        elif profile.company in ['TCS', 'Infosys', 'Wipro']:
            notes.append("Emphasize domain expertise and client interaction")
            notes.append("Include project delivery experience")
        return notes

    # ---------------- ATS PROFILES ----------------
    def _initialize_ats_profiles(self) -> Dict[str, ATSProfile]:
        return {
            # (Here we paste your full original profiles exactly as they were in your old file)
            # Amazon, Google, Microsoft, TCS, Infosys, Wipro, IBM, Accenture, Generic...
            #  (your original dictionary content goes here exactly unchanged)
        }
