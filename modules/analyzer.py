"""
Analyzer Module
Coordinates resume parsing, ATS simulation, keyword gap analysis, and recommendations.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from .company_ats import CompanyATS, ATSProfile  # <-- FIXED: added ATSProfile
import re


@dataclass
class AnalysisResult:
    company: str
    overall_score: float
    ats_results: Dict
    section_analysis: Dict
    keyword_gaps: Dict
    recommendations: List[Dict]
    resume_summary: Dict


class ResumeAnalyzer:
    def __init__(self):
        self.company_ats = CompanyATS()

    def analyze_resume(
        self,
        resume_data: Dict,
        company: str,
        job_description: Optional[str] = None
    ) -> AnalysisResult:
        """Run full resume analysis workflow."""
        # Normalize sections to avoid type mismatch
        if "sections" in resume_data:
            resume_data["sections"] = self._normalize_sections(resume_data["sections"])

        ats_results = self.company_ats.simulate_ats_filtering(resume_data, company)

        section_analysis = self._analyze_sections(resume_data, ats_results["ats_profile"])
        keyword_gaps = self._analyze_keywords(resume_data, ats_results["ats_profile"], job_description)
        recommendations = self._generate_recommendations(section_analysis, keyword_gaps)

        overall_score = self._calculate_overall_score(ats_results, section_analysis)

        resume_summary = {
            "total_experience": resume_data.get("experience_years", 0),
            "skill_count": len(resume_data.get("skills", [])),
            "section_count": len([sec for sec in resume_data.get("sections", {}) if resume_data["sections"][sec]]),
        }

        return AnalysisResult(
            company=company,
            overall_score=overall_score,
            ats_results=ats_results,
            section_analysis=section_analysis,
            keyword_gaps=keyword_gaps,
            recommendations=recommendations,
            resume_summary=resume_summary
        )

    def _normalize_sections(self, sections: Dict) -> Dict:
        """Ensure sections dict is in a consistent format."""
        normalized = {}
        for key, value in sections.items():
            if isinstance(value, str):
                normalized[key] = {"present": bool(value.strip()), "text": value, "word_count": len(value.split())}
            elif isinstance(value, dict):
                normalized[key] = value
            else:
                normalized[key] = {"present": bool(value), "text": "", "word_count": 0}
        return normalized

    def _analyze_sections(self, resume_data: Dict, ats_profile: ATSProfile) -> Dict:
        """Evaluate each resume section for completeness and strength."""
        section_analysis = {}
        for section_name, section_info in resume_data.get("sections", {}).items():
            present = section_info["present"]
            text = section_info.get("text", "")
            word_count = section_info.get("word_count", 0)

            strength = self._assess_section_strength(section_name, word_count)
            suggestions = self._get_section_suggestions(section_name, strength, ats_profile)

            section_analysis[section_name] = {
                "present": present,
                "strength": strength,
                "word_count": word_count,
                "suggestions": suggestions
            }
        return section_analysis

    def _assess_section_strength(self, section_name: str, word_count: int) -> str:
        """Heuristic to rate section strength."""
        if word_count > 100:
            return "Excellent"
        elif word_count > 50:
            return "Good"
        elif word_count > 20:
            return "Fair"
        elif word_count > 0:
            return "Poor"
        else:
            return "Poor"

    def _get_section_suggestions(
        self,
        section_name: str,
        strength: str,
        ats_profile: ATSProfile
    ) -> List[str]:
        """Provide section-specific improvement suggestions."""
        suggestions = []
        if not strength or strength in ["Poor", "Fair"]:
            suggestions.append(f"Enhance {section_name} section with more relevant details and keywords.")
        # Example: match ATS-required keywords
        if ats_profile.required_keywords:
            suggestions.append(f"Include role-specific keywords for {section_name}.")
        return suggestions

    def _analyze_keywords(
        self,
        resume_data: Dict,
        ats_profile: ATSProfile,
        job_description: Optional[str]
    ) -> Dict:
        """Compare resume keywords with ATS/company requirements and job description."""
        company_keywords = ats_profile.required_keywords
        resume_text = " ".join([sec.get("text", "") for sec in resume_data["sections"].values()])

        matched_company_keywords = [kw for kw in company_keywords if kw.lower() in resume_text.lower()]
        missing_company_keywords = [kw for kw in company_keywords if kw.lower() not in resume_text.lower()]

        jd_skill_match_percentage = None
        missing_jd_skills = []
        if job_description:
            jd_keywords = self._extract_keywords_from_jd(job_description)
            matched_jd = [kw for kw in jd_keywords if kw.lower() in resume_text.lower()]
            missing_jd_skills = [kw for kw in jd_keywords if kw.lower() not in resume_text.lower()]
            if jd_keywords:
                jd_skill_match_percentage = (len(matched_jd) / len(jd_keywords)) * 100

        keyword_match_percentage = (len(matched_company_keywords) / len(company_keywords) * 100) if company_keywords else 0

        return {
            "keyword_match_percentage": keyword_match_percentage,
            "matched_company_keywords": matched_company_keywords,
            "missing_company_keywords": missing_company_keywords,
            "jd_skill_match_percentage": jd_skill_match_percentage,
            "missing_jd_skills": missing_jd_skills
        }

    def _extract_keywords_from_jd(self, job_description: str) -> List[str]:
        """Naive keyword extraction from job description."""
        words = re.findall(r"[A-Za-z]+", job_description)
        # Remove common words
        stopwords = {"and", "the", "to", "of", "in", "for", "with", "on", "at", "by"}
        return [w for w in words if w.lower() not in stopwords and len(w) > 2]

    def _generate_recommendations(
        self,
        section_analysis: Dict,
        keyword_gaps: Dict
    ) -> List[Dict]:
        """Create actionable recommendations based on gaps."""
        recs = []
        # Section improvements
        for section, data in section_analysis.items():
            if not data["present"] or data["strength"] in ["Poor", "Fair"]:
                recs.append({
                    "priority": "High",
                    "title": f"Improve {section} section",
                    "category": "Content",
                    "description": f"The {section} section is {data['strength']}. Add more details and relevant keywords.",
                    "action_items": [
                        f"Expand on your {section} experience",
                        f"Add quantifiable achievements",
                        "Align content with job requirements"
                    ]
                })
        # Keyword gaps
        if keyword_gaps["missing_company_keywords"]:
            recs.append({
                "priority": "High",
                "title": "Add missing company-required keywords",
                "category": "Keywords",
                "description": "Include these missing company-specific keywords to improve ATS match.",
                "action_items": keyword_gaps["missing_company_keywords"]
            })
        if keyword_gaps.get("missing_jd_skills"):
            recs.append({
                "priority": "Medium",
                "title": "Add missing job-specific skills",
                "category": "Keywords",
                "description": "Incorporate these skills from the job description.",
                "action_items": keyword_gaps["missing_jd_skills"]
            })
        return recs

    def _calculate_overall_score(self, ats_results: Dict, section_analysis: Dict) -> float:
        """Compute weighted overall score."""
        ats_score = ats_results["overall_ats_score"]
        section_score = sum(
            {"Excellent": 100, "Good": 80, "Fair": 60, "Poor": 40}.get(data["strength"], 0)
            for data in section_analysis.values()
        ) / max(len(section_analysis), 1)
        return round((ats_score * 0.7) + (section_score * 0.3), 2)


if __name__ == "__main__":
    print("Analyzer module is not meant to be run standalone.")
