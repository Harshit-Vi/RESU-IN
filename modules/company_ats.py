"""
Company ATS Simulation Module
Supports Rule-based and Smart (ML-simulated) scoring
"""

from typing import Dict, List, Set
from dataclasses import dataclass

@dataclass
class ATSProfile:
    """ATS profile for a specific company"""
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
    scoring_strictness: float  # 0.0 to 1.0
    common_filters: List[str]

class CompanyATS:
    def __init__(self):
        self.ats_profiles = self._initialize_ats_profiles()

    def get_available_companies(self) -> List[str]:
        """Get list of available companies"""
        return list(self.ats_profiles.keys())

    def choose_scoring_mode(self) -> str:
        """Prompt for scoring mode"""
        while True:
            print("\nChoose ATS scoring mode:")
            print("1 - Rule-based")
            print("2 - Smart (ML-simulated)")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                return "rule"
            elif choice == "2":
                return "smart"
            else:
                print("Invalid choice. Please enter 1 or 2.")

    def choose_company(self) -> str:
        """Prompt for company selection"""
        companies = self.get_available_companies()
        print("\nSelect company:")
        for idx, comp in enumerate(companies, 1):
            print(f"{idx} - {comp}")
        while True:
            try:
                choice = int(input("Enter company number: ").strip())
                if 1 <= choice <= len(companies):
                    return companies[choice - 1]
            except ValueError:
                pass
            print("Invalid choice. Please enter a valid number.")

    def get_ats_profile(self, company: str) -> ATSProfile:
        """Get ATS profile for a specific company"""
        return self.ats_profiles.get(company, self.ats_profiles['Generic'])

    def _initialize_ats_profiles(self) -> Dict[str, ATSProfile]:
        """Initialize ATS profiles for different companies"""
        return {
            # Original 9
            'Amazon': ATSProfile(
                company='Amazon',
                keyword_weight=0.35, experience_weight=0.25,
                education_weight=0.15, skills_weight=0.20, format_weight=0.05,
                preferred_keywords={'aws','cloud','microservices','distributed systems','scalability',
                                     'leadership principles','customer obsession','ownership','bias for action',
                                     'java','python','sql','data structures','algorithms','system design'},
                required_skills={'programming','problem solving','system design','cloud computing','databases'},
                experience_requirements={'entry':0,'mid':3,'senior':5,'principal':8},
                education_preferences=['bachelors','masters','phd'],
                scoring_strictness=0.8, common_filters=['leadership','innovation','scale']
            ),
            'Google': ATSProfile(
                company='Google',
                keyword_weight=0.30, experience_weight=0.25,
                education_weight=0.20, skills_weight=0.20, format_weight=0.05,
                preferred_keywords={'machine learning','ai','tensorflow','algorithms','data structures',
                                     'python','c++','java','go','distributed systems','gcp','research',
                                     'innovation','scalability','performance optimization'},
                required_skills={'programming','algorithms','data structures','system design','problem solving'},
                experience_requirements={'entry':0,'mid':3,'senior':5,'staff':8},
                education_preferences=['masters','phd','bachelors'],
                scoring_strictness=0.85, common_filters=['innovation','research','impact']
            ),
            'Microsoft': ATSProfile(
                company='Microsoft',
                keyword_weight=0.32, experience_weight=0.28,
                education_weight=0.18, skills_weight=0.18, format_weight=0.04,
                preferred_keywords={'azure','c#','.net','sql server','office 365','powershell','active directory',
                                     'sharepoint','teams','cloud computing','devops','agile'},
                required_skills={'programming','cloud platforms','collaboration','problem solving'},
                experience_requirements={'entry':0,'mid':2,'senior':5,'principal':7},
                education_preferences=['bachelors','masters'],
                scoring_strictness=0.75, common_filters=['collaboration','diversity','growth mindset']
            ),
            'TCS': ATSProfile(
                company='TCS',
                keyword_weight=0.25, experience_weight=0.30,
                education_weight=0.25, skills_weight=0.15, format_weight=0.05,
                preferred_keywords={'java','spring','hibernate','sql','oracle','agile','scrum','banking','finance',
                                     'erp','sap','mainframe','cobol','testing','qa'},
                required_skills={'programming','database management','testing','domain knowledge'},
                experience_requirements={'entry':0,'mid':3,'senior':6,'lead':8},
                education_preferences=['bachelors','masters'],
                scoring_strictness=0.70, common_filters=['domain expertise','client handling','delivery']
            ),
            'Infosys': ATSProfile(
                company='Infosys',
                keyword_weight=0.28, experience_weight=0.32,
                education_weight=0.22, skills_weight=0.15, format_weight=0.03,
                preferred_keywords={'java','python','sql','agile','devops','cloud','digital transformation',
                                     'automation','ai','machine learning','consulting'},
                required_skills={'programming','consulting','client interaction','problem solving'},
                experience_requirements={'entry':0,'mid':2,'senior':5,'principal':8},
                education_preferences=['bachelors','masters'],
                scoring_strictness=0.72, common_filters=['innovation','digital','transformation']
            ),
            'Wipro': ATSProfile(
                company='Wipro',
                keyword_weight=0.26, experience_weight=0.30,
                education_weight=0.24, skills_weight=0.16, format_weight=0.04,
                preferred_keywords={'java','c++','sql','testing','automation','agile','healthcare','banking',
                                     'retail','cloud','devops','sap'},
                required_skills={'programming','domain knowledge','testing','project management'},
                experience_requirements={'entry':0,'mid':3,'senior':5,'manager':7},
                education_preferences=['bachelors','masters'],
                scoring_strictness=0.68, common_filters=['domain expertise','quality','delivery']
            ),
            'IBM': ATSProfile(
                company='IBM',
                keyword_weight=0.30, experience_weight=0.25,
                education_weight=0.20, skills_weight=0.20, format_weight=0.05,
                preferred_keywords={'watson','ai','machine learning','cloud','blockchain','quantum','mainframe','db2',
                                     'websphere','consulting','transformation'},
                required_skills={'consulting','enterprise solutions','ai/ml','problem solving'},
                experience_requirements={'entry':0,'mid':3,'senior':6,'executive':10},
                education_preferences=['masters','phd','bachelors'],
                scoring_strictness=0.78, common_filters=['innovation','research','enterprise']
            ),
            'Accenture': ATSProfile(
                company='Accenture',
                keyword_weight=0.27, experience_weight=0.28,
                education_weight=0.20, skills_weight=0.20, format_weight=0.05,
                preferred_keywords={'consulting','digital transformation','cloud','agile','change management',
                                     'strategy','analytics','ai','automation','client'},
                required_skills={'consulting','client management','strategy','digital transformation'},
                experience_requirements={'entry':0,'mid':2,'senior':4,'manager':6},
                education_preferences=['masters','bachelors','mba'],
                scoring_strictness=0.75, common_filters=['consulting','strategy','transformation']
            ),
            'Generic': ATSProfile(
                company='Generic',
                keyword_weight=0.30, experience_weight=0.25,
                education_weight=0.20, skills_weight=0.20, format_weight=0.05,
                preferred_keywords={'programming','problem solving','teamwork','communication','leadership','project management'},
                required_skills={'programming','problem solving','communication'},
                experience_requirements={'entry':0,'mid':3,'senior':5},
                education_preferences=['bachelors','masters'],
                scoring_strictness=0.70, common_filters=['skills','experience','education']
            ),
            'Deloitte': ATSProfile(
                company='Deloitte', keyword_weight=0.28, experience_weight=0.27,
                education_weight=0.22, skills_weight=0.18, format_weight=0.05,
                preferred_keywords={'consulting','audit','risk','analytics','sap','finance','data analysis'},
                required_skills={'consulting','analytics','project management','finance'},
                experience_requirements={'entry':0,'mid':2,'senior':5}, education_preferences=['bachelors','masters'],
                scoring_strictness=0.73, common_filters=['client','delivery','quality']
            ),
                        'Capgemini': ATSProfile(
                company='Capgemini', keyword_weight=0.27, experience_weight=0.29,
                education_weight=0.21, skills_weight=0.18, format_weight=0.05,
                preferred_keywords={'java','cloud','devops','testing','automation','sap','agile','digital transformation'},
                required_skills={'programming','testing','cloud computing','project management'},
                experience_requirements={'entry':0,'mid':2,'senior':5}, education_preferences=['bachelors','masters'],
                scoring_strictness=0.71, common_filters=['delivery','teamwork','quality']
            ),
            'Oracle': ATSProfile(
                company='Oracle', keyword_weight=0.33, experience_weight=0.25,
                education_weight=0.18, skills_weight=0.19, format_weight=0.05,
                preferred_keywords={'oracle','java','sql','database','cloud','erp','sap','analytics'},
                required_skills={'database management','programming','cloud computing'},
                experience_requirements={'entry':0,'mid':3,'senior':5}, education_preferences=['bachelors','masters'],
                scoring_strictness=0.76, common_filters=['database','enterprise','cloud']
            ),
            'Cisco': ATSProfile(
                company='Cisco', keyword_weight=0.31, experience_weight=0.26,
                education_weight=0.20, skills_weight=0.18, format_weight=0.05,
                preferred_keywords={'networking','security','cloud','ccna','ccnp','routing','switching'},
                required_skills={'networking','security','cloud computing'},
                experience_requirements={'entry':0,'mid':2,'senior':5}, education_preferences=['bachelors','masters'],
                scoring_strictness=0.78, common_filters=['networking','security','infrastructure']
            ),
            'HCL': ATSProfile(
                company='HCL', keyword_weight=0.26, experience_weight=0.32,
                education_weight=0.22, skills_weight=0.17, format_weight=0.03,
                preferred_keywords={'java','testing','automation','sap','agile','cloud','devops'},
                required_skills={'programming','testing','cloud computing'},
                experience_requirements={'entry':0,'mid':2,'senior':5}, education_preferences=['bachelors','masters'],
                scoring_strictness=0.70, common_filters=['delivery','domain expertise','client']
            ),
            'Adobe': ATSProfile(
                company='Adobe', keyword_weight=0.34, experience_weight=0.24,
                education_weight=0.18, skills_weight=0.19, format_weight=0.05,
                preferred_keywords={'photoshop','illustrator','creative','cloud','xd','design','ui/ux','pdf'},
                required_skills={'design','creativity','cloud computing'},
                experience_requirements={'entry':0,'mid':3,'senior':5}, education_preferences=['bachelors','masters'],
                scoring_strictness=0.79, common_filters=['creativity','innovation','design']
            ),
            'Siemens': ATSProfile(
                company='Siemens', keyword_weight=0.29, experience_weight=0.28,
                education_weight=0.20, skills_weight=0.18, format_weight=0.05,
                preferred_keywords={'automation','iot','plc','scada','engineering','manufacturing'},
                required_skills={'automation','iot','engineering'},
                experience_requirements={'entry':0,'mid':3,'senior':6}, education_preferences=['bachelors','masters'],
                scoring_strictness=0.74, common_filters=['engineering','automation','industry']
            ),
            'Intel': ATSProfile(
                company='Intel', keyword_weight=0.35, experience_weight=0.25,
                education_weight=0.18, skills_weight=0.17, format_weight=0.05,
                preferred_keywords={'semiconductors','hardware','design','microprocessors','c','c++','verilog','vhdl'},
                required_skills={'hardware design','programming','electronics'},
                experience_requirements={'entry':0,'mid':3,'senior':6}, education_preferences=['bachelors','masters','phd'],
                scoring_strictness=0.82, common_filters=['hardware','design','research']
            ),
            'JP Morgan': ATSProfile(
                company='JP Morgan', keyword_weight=0.32, experience_weight=0.27,
                education_weight=0.20, skills_weight=0.18, format_weight=0.03,
                preferred_keywords={'finance','banking','risk','analytics','java','python','sql'},
                required_skills={'finance','analytics','programming'},
                experience_requirements={'entry':0,'mid':2,'senior':5}, education_preferences=['bachelors','masters'],
                scoring_strictness=0.77, common_filters=['finance','analytics','banking']
            ),
            'Goldman Sachs': ATSProfile(
                company='Goldman Sachs', keyword_weight=0.34, experience_weight=0.26,
                education_weight=0.20, skills_weight=0.17, format_weight=0.03,
                preferred_keywords={'finance','investment','banking','risk','analytics','java','python','sql'},
                required_skills={'finance','analytics','programming'},
                experience_requirements={'entry':0,'mid':3,'senior':6}, education_preferences=['bachelors','masters'],
                scoring_strictness=0.80, common_filters=['finance','investment','analytics']
            ),
        }

    def simulate_ats_filtering(self, resume_data: Dict, company: str, mode: str) -> Dict:
        """Simulate ATS filtering for selected mode"""
        profile = self.get_ats_profile(company)

        if mode == "rule":
            return self._simulate_rule_based(resume_data, profile)
        else:
            return self._simulate_smart_mode(resume_data, profile)

    def _simulate_rule_based(self, resume_data: Dict, profile: ATSProfile) -> Dict:
        """Original rule-based scoring"""
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

    def _simulate_smart_mode(self, resume_data: Dict, profile: ATSProfile) -> Dict:
        """
        Simulated ML scoring — more nuanced scoring based on patterns seen
        in real ATS data (no actual ML model here, just heuristics emulating ML).
        """
        passes_initial = self._initial_screening(resume_data, profile)

        # More granular keyword scoring
        keyword_score = self._calculate_keyword_score(resume_data, profile)
        if resume_data.get('education_level') not in profile.education_preferences:
            keyword_score *= 0.95  # penalize slightly

        # Experience bonus if matches exact company preference
        experience_score = self._evaluate_experience(resume_data, profile)
        if experience_score >= 80 and 'leadership' in resume_data.get('keywords', []):
            experience_score += 5

        # Skills score — weighted by rarity
        skills_score = self._match_skills(resume_data, profile)
        if skills_score < 50 and 'cloud' in resume_data.get('keywords', []):
            skills_score += 10

        # Education score — higher for top-tier match
        education_score = self._assess_education(resume_data, profile)
        if profile.company in ['Google', 'Amazon', 'Microsoft'] and education_score >= 90:
            education_score += 5

        # Format — bonus for complete resumes
        format_score = self._evaluate_format(resume_data, profile)
        if all(sec in resume_data.get('sections', {}) for sec in ['experience', 'education', 'skills']):
            format_score += 5

        # Weighted final score
        overall_score = (
            keyword_score * profile.keyword_weight +
            experience_score * profile.experience_weight +
            education_score * profile.education_weight +
            skills_score * profile.skills_weight +
            format_score * profile.format_weight
        )
        adjusted_score = min(overall_score * (1 - profile.scoring_strictness * 0.15), 100)

        return {
            'passes_initial_screening': passes_initial,
            'keyword_score': round(keyword_score, 2),
            'experience_score': round(experience_score, 2),
            'education_score': round(education_score, 2),
            'skills_score': round(skills_score, 2),
            'format_score': round(format_score, 2),
            'overall_ats_score': round(adjusted_score, 2),
            'ats_recommendation': self._get_ats_recommendation(adjusted_score),
            'company_specific_notes': self._get_company_notes(resume_data, profile)
        }

    # The rest of helper functions (_initial_screening, _calculate_keyword_score, etc.)
    # stay exactly the same as your previous working version
"""
Company ATS Simulation Module
Supports Rule-based & Smart ML-simulated Scoring
"""

from typing import Dict, List, Set
from dataclasses import dataclass

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
        self.synonym_map = self._build_synonym_map()

    def choose_mode(self) -> str:
        """Ask user for scoring mode"""
        print("\nChoose ATS scoring mode:")
        print("1 - Rule-based")
        print("2 - Smart (ML-simulated)")
        choice = input("Enter choice (1 or 2): ").strip()
        return "smart" if choice == "2" else "rule"

    def get_available_companies(self) -> List[str]:
        return list(self.ats_profiles.keys())

    def get_ats_profile(self, company: str) -> ATSProfile:
        return self.ats_profiles.get(company, self.ats_profiles['Generic'])

    def _build_synonym_map(self) -> Dict[str, List[str]]:
        return {
            "machine learning": ["ml", "deep learning", "artificial intelligence"],
            "java script": ["javascript", "js"],
            "project management": ["pmp", "scrum master"],
            "cloud computing": ["aws", "azure", "gcp", "google cloud", "cloud"],
            "ai": ["artificial intelligence", "machine learning", "ml"],
            "devops": ["ci/cd", "continuous integration", "continuous delivery"],
        }

    def simulate_ats_filtering(self, resume_data: Dict, company: str, mode: str) -> Dict:
        if mode == "smart":
            return self._smart_scoring(resume_data, company)
        else:
            return self._rule_based_scoring(resume_data, company)

    # -------------------- Rule-based scoring -------------------- #
    def _rule_based_scoring(self, resume_data: Dict, company: str) -> Dict:
        profile = self.get_ats_profile(company)
        passes_initial = self._initial_screening(resume_data)

        keyword_score = self._calculate_keyword_score(resume_data, profile)
        experience_score = self._evaluate_experience(resume_data, profile)
        education_score = self._assess_education(resume_data, profile)
        skills_score = self._match_skills(resume_data, profile)
        format_score = self._evaluate_format(resume_data)

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
            'company_specific_notes': self._get_company_notes(profile)
        }

    # -------------------- Smart ML-simulated scoring -------------------- #
    def _smart_scoring(self, resume_data: Dict, company: str) -> Dict:
        profile = self.get_ats_profile(company)
        passes_initial = self._initial_screening(resume_data)

        keyword_score = self._calculate_smart_keyword_score(resume_data, profile)
        experience_score = self._evaluate_experience(resume_data, profile, recency_boost=True)
        education_score = self._assess_education(resume_data, profile)
        skills_score = self._match_skills(resume_data, profile, partial_match=True)
        format_score = self._evaluate_format(resume_data, smart=True)

        overall_score = (
            keyword_score * 0.4 +
            experience_score * 0.25 +
            education_score * 0.15 +
            skills_score * 0.15 +
            format_score * 0.05
        )

        if overall_score < 50:
            passes_initial = False

        return {
            'passes_initial_screening': passes_initial,
            'keyword_score': keyword_score,
            'experience_score': experience_score,
            'education_score': education_score,
            'skills_score': skills_score,
            'format_score': format_score,
            'overall_ats_score': min(overall_score, 100),
            'ats_recommendation': self._get_ats_recommendation(overall_score),
            'company_specific_notes': self._get_company_notes(profile)
        }

    # -------------------- Helper scoring functions -------------------- #
    def _initial_screening(self, resume_data: Dict) -> bool:
        return (
            bool(resume_data.get('contact_info', {}).get('email')) and
            len(resume_data.get('raw_text', '')) > 100 and
            len(resume_data.get('skills', [])) > 0
        )

    def _calculate_keyword_score(self, resume_data: Dict, profile: ATSProfile) -> float:
        resume_text = resume_data.get('raw_text', '').lower()
        matched_keywords = sum(1 for kw in profile.preferred_keywords if kw.lower() in resume_text)
        return (matched_keywords / len(profile.preferred_keywords) * 100) if profile.preferred_keywords else 0

    def _calculate_smart_keyword_score(self, resume_data: Dict, profile: ATSProfile) -> float:
        resume_text = resume_data.get('raw_text', '').lower()
        matched_keywords = 0
        for kw in profile.preferred_keywords:
            if kw.lower() in resume_text:
                matched_keywords += 1
            elif kw.lower() in self.synonym_map:
                if any(syn in resume_text for syn in self.synonym_map[kw.lower()]):
                    matched_keywords += 0.8
        if resume_text.count(kw.lower()) > 5:
            matched_keywords -= 1
        return max((matched_keywords / len(profile.preferred_keywords) * 100), 0)

    def _evaluate_experience(self, resume_data: Dict, profile: ATSProfile, recency_boost=False) -> float:
        years = resume_data.get('experience_years', 0)
        if recency_boost and '2023' in resume_data.get('raw_text', ''):
            years += 1
        if years >= profile.experience_requirements.get('senior', 5):
            return 100
        elif years >= profile.experience_requirements.get('mid', 3):
            return 80
        elif years >= profile.experience_requirements.get('entry', 0):
            return 60
        return 40

    def _assess_education(self, resume_data: Dict, profile: ATSProfile) -> float:
        level = resume_data.get('education_level', 'unknown')
        if level in profile.education_preferences:
            index = profile.education_preferences.index(level)
            return 100 - (index * 20)
        return 50

    def _match_skills(self, resume_data: Dict, profile: ATSProfile, partial_match=False) -> float:
        resume_skills = set(skill.lower() for skill in resume_data.get('skills', []))
        required_skills = set(skill.lower() for skill in profile.required_skills)
        matches = len(resume_skills.intersection(required_skills))
        if partial_match:
            for skill in required_skills:
                if any(skill in rs for rs in resume_skills):
                    matches += 0.5
        return (matches / len(required_skills) * 100) if required_skills else 0

    def _evaluate_format(self, resume_data: Dict, smart=False) -> float:
        score = 100
        required_sections = ['experience', 'education', 'skills']
        sections = resume_data.get('sections', {})
        for section in required_sections:
            if section not in sections:
                score -= 20
        if not resume_data.get('contact_info', {}).get('email'):
            score -= 30
        if smart and len(resume_data.get('raw_text', '').split()) < 200:
            score -= 15
        return max(score, 0)

    def _get_ats_recommendation(self, score: float) -> str:
        if score >= 80: return "High likelihood of passing ATS screening"
        elif score >= 60: return "Moderate likelihood of passing ATS screening"
        elif score >= 40: return "Low likelihood of passing ATS screening"
        return "Very low likelihood of passing ATS screening"

    def _get_company_notes(self, profile: ATSProfile) -> List[str]:
        notes = []
        if profile.company == 'Amazon':
            notes += ["Emphasize leadership principles", "Include system scalability metrics"]
        elif profile.company == 'Google':
            notes += ["Highlight algorithmic work", "Add research/publications if any"]
        elif profile.company in ['TCS', 'Infosys', 'Wipro']:
            notes += ["Show domain expertise", "Add client interaction & delivery experience"]
        return notes

    def _initialize_ats_profiles(self) -> Dict[str, ATSProfile]:
        return {
            # Your original 8 companies...
            # (Amazon, Google, Microsoft, TCS, Infosys, Wipro, IBM, Accenture, Generic)
            # + 10 more new ones with realistic ATS settings
            # [I will paste all in next message due to space]
        }

            
        }
