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
    """Main ATS simulation class with rule-based and smart scoring modes"""
    
    def __init__(self):
        self.ats_profiles = self._initialize_ats_profiles()
        self.synonym_map = self._build_synonym_map()

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

    def simulate_ats_filtering(self, resume_data: Dict, company: str = "Generic", mode: str = "rule") -> Dict:
        """
        Simulate ATS filtering for selected mode
        
        Args:
            resume_data (Dict): Resume data to analyze
            company (str): Company name (default: "Generic")
            mode (str): Scoring mode - "rule" or "smart" (default: "rule")
        
        Returns:
            Dict: ATS scoring results
        """
        # Input validation
        if not isinstance(resume_data, dict):
            raise ValueError("resume_data must be a dictionary")
        
        if company not in self.ats_profiles:
            print(f"Warning: Company '{company}' not found. Using Generic profile.")
            company = "Generic"
        
        if mode not in ["rule", "smart"]:
            print(f"Warning: Invalid mode '{mode}'. Using 'rule' mode.")
            mode = "rule"
        
        profile = self.get_ats_profile(company)

        if mode == "rule":
            return self._simulate_rule_based(resume_data, profile)
        else:
            return self._simulate_smart_mode(resume_data, profile)

    # ==================== RULE-BASED SCORING ====================
    
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
            'keyword_score': round(keyword_score, 2),
            'experience_score': round(experience_score, 2),
            'education_score': round(education_score, 2),
            'skills_score': round(skills_score, 2),
            'format_score': round(format_score, 2),
            'overall_ats_score': round(min(adjusted_score, 100), 2),
            'ats_recommendation': self._get_ats_recommendation(adjusted_score),
            'company_specific_notes': self._get_company_notes(resume_data, profile)
        }

    # ==================== SMART MODE SCORING ====================
    
    def _simulate_smart_mode(self, resume_data: Dict, profile: ATSProfile) -> Dict:
        """
        Simulated ML scoring — more nuanced scoring based on patterns seen
        in real ATS data (no actual ML model here, just heuristics emulating ML).
        """
        passes_initial = self._initial_screening(resume_data, profile)

        # More granular keyword scoring with synonyms
        keyword_score = self._calculate_smart_keyword_score(resume_data, profile)
        
        # Experience scoring with recency boost
        experience_score = self._evaluate_smart_experience(resume_data, profile)
        
        # Education score with tier matching
        education_score = self._assess_smart_education(resume_data, profile)
        
        # Skills score with partial matching
        skills_score = self._match_smart_skills(resume_data, profile)
        
        # Format score with completeness bonus
        format_score = self._evaluate_smart_format(resume_data, profile)

        # Weighted final score with smart adjustments
        overall_score = (
            keyword_score * profile.keyword_weight +
            experience_score * profile.experience_weight +
            education_score * profile.education_weight +
            skills_score * profile.skills_weight +
            format_score * profile.format_weight
        )
        
        # Apply company-specific smart adjustments
        overall_score = self._apply_smart_adjustments(overall_score, resume_data, profile)
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

    # ==================== HELPER FUNCTIONS ====================
    
    def _initial_screening(self, resume_data: Dict, profile: ATSProfile) -> bool:
        """Basic initial screening checks"""
        return (
            bool(resume_data.get('contact_info', {}).get('email')) and
            len(resume_data.get('raw_text', '')) > 100 and
            len(resume_data.get('skills', [])) > 0
        )

    def _calculate_keyword_score(self, resume_data: Dict, profile: ATSProfile) -> float:
        """Calculate keyword matching score (rule-based)"""
        resume_text = resume_data.get('raw_text', '').lower()
        matched_keywords = sum(1 for kw in profile.preferred_keywords 
                             if kw.lower() in resume_text)
        return (matched_keywords / len(profile.preferred_keywords) * 100) if profile.preferred_keywords else 0

    def _calculate_smart_keyword_score(self, resume_data: Dict, profile: ATSProfile) -> float:
        """Calculate keyword matching score with synonyms and context"""
        resume_text = resume_data.get('raw_text', '').lower()
        matched_keywords = 0
        
        for kw in profile.preferred_keywords:
            if kw.lower() in resume_text:
                # Full match
                matched_keywords += 1
            elif kw.lower() in self.synonym_map:
                # Synonym match (partial credit)
                if any(syn in resume_text for syn in self.synonym_map[kw.lower()]):
                    matched_keywords += 0.8
        
        # Penalty for keyword stuffing
        total_words = len(resume_text.split())
        if total_words > 0:
            keyword_density = sum(resume_text.count(kw.lower()) for kw in profile.preferred_keywords) / total_words
            if keyword_density > 0.1:  # More than 10% keyword density
                matched_keywords *= 0.9
        
        return max((matched_keywords / len(profile.preferred_keywords) * 100), 0) if profile.preferred_keywords else 0

    def _evaluate_experience(self, resume_data: Dict, profile: ATSProfile) -> float:
        """Evaluate experience level (rule-based)"""
        years = resume_data.get('experience_years', 0)
        
        if years >= profile.experience_requirements.get('senior', 5):
            return 100
        elif years >= profile.experience_requirements.get('mid', 3):
            return 80
        elif years >= profile.experience_requirements.get('entry', 0):
            return 60
        return 40

    def _evaluate_smart_experience(self, resume_data: Dict, profile: ATSProfile) -> float:
        """Evaluate experience with recency and relevance boost"""
        base_score = self._evaluate_experience(resume_data, profile)
        
        # Bonus for recent experience
        resume_text = resume_data.get('raw_text', '')
        if any(year in resume_text for year in ['2023', '2024', '2025']):
            base_score += 5
        
        # Bonus for leadership keywords
        leadership_keywords = ['lead', 'manage', 'director', 'senior', 'principal']
        if any(kw in resume_text.lower() for kw in leadership_keywords):
            base_score += 10
        
        return min(base_score, 100)

    def _assess_education(self, resume_data: Dict, profile: ATSProfile) -> float:
        """Assess education level (rule-based)"""
        level = resume_data.get('education_level', 'unknown').lower()
        
        for i, pref in enumerate(profile.education_preferences):
            if pref.lower() in level:
                return 100 - (i * 15)  # Higher preference = higher score
        return 50  # Default score for unknown/other education

    def _assess_smart_education(self, resume_data: Dict, profile: ATSProfile) -> float:
        """Assess education with tier matching bonus"""
        base_score = self._assess_education(resume_data, profile)
        
        # Bonus for top-tier companies expecting high education
        if (profile.company in ['Google', 'Amazon', 'Microsoft', 'Goldman Sachs'] and 
            base_score >= 85):
            base_score += 10
        
        return min(base_score, 100)

    def _match_skills(self, resume_data: Dict, profile: ATSProfile) -> float:
        """Match required skills (rule-based)"""
        resume_skills = set(skill.lower() for skill in resume_data.get('skills', []))
        required_skills = set(skill.lower() for skill in profile.required_skills)
        matches = len(resume_skills.intersection(required_skills))
        return (matches / len(required_skills) * 100) if required_skills else 0

    def _match_smart_skills(self, resume_data: Dict, profile: ATSProfile) -> float:
        """Match skills with partial matching"""
        base_score = self._match_skills(resume_data, profile)
        
        # Partial matching bonus
        resume_skills = [skill.lower() for skill in resume_data.get('skills', [])]
        resume_text = resume_data.get('raw_text', '').lower()
        
        partial_matches = 0
        for req_skill in profile.required_skills:
            if any(req_skill.lower() in skill for skill in resume_skills):
                partial_matches += 0.5
            elif req_skill.lower() in resume_text:
                partial_matches += 0.3
        
        bonus_score = (partial_matches / len(profile.required_skills) * 20) if profile.required_skills else 0
        return min(base_score + bonus_score, 100)

    def _evaluate_format(self, resume_data: Dict, profile: ATSProfile) -> float:
        """Evaluate resume format (rule-based)"""
        score = 100
        
        # Check for required sections
        sections = resume_data.get('sections', {})
        required_sections = ['experience', 'education', 'skills']
        for section in required_sections:
            if section not in sections:
                score -= 25
        
        # Check for contact information
        if not resume_data.get('contact_info', {}).get('email'):
            score -= 30
        
        return max(score, 0)

    def _evaluate_smart_format(self, resume_data: Dict, profile: ATSProfile) -> float:
        """Evaluate format with completeness bonus"""
        base_score = self._evaluate_format(resume_data, profile)
        
        # Bonus for comprehensive resumes
        if all(section in resume_data.get('sections', {}) 
               for section in ['experience', 'education', 'skills', 'summary']):
            base_score += 10
        
        # Penalty for too short resumes
        if len(resume_data.get('raw_text', '').split()) < 200:
            base_score -= 15
        
        return max(min(base_score, 100), 0)

    def _apply_smart_adjustments(self, score: float, resume_data: Dict, profile: ATSProfile) -> float:
        """Apply company-specific smart adjustments"""
        # Cloud experience bonus for tech companies
        if (profile.company in ['Amazon', 'Google', 'Microsoft'] and 
            'cloud' in resume_data.get('raw_text', '').lower()):
            score += 5
        
        # Domain expertise bonus for consulting companies
        if (profile.company in ['Accenture', 'Deloitte'] and 
            'consulting' in resume_data.get('raw_text', '').lower()):
            score += 5
        
        # Finance experience bonus for financial companies
        if (profile.company in ['JP Morgan', 'Goldman Sachs'] and 
            any(term in resume_data.get('raw_text', '').lower() 
                for term in ['finance', 'banking', 'investment'])):
            score += 5
        
        return score

    def _get_ats_recommendation(self, score: float) -> str:
        """Get ATS recommendation based on score"""
        if score >= 80:
            return "High likelihood of passing ATS screening"
        elif score >= 60:
            return "Moderate likelihood of passing ATS screening"
        elif score >= 40:
            return "Low likelihood of passing ATS screening"
        return "Very low likelihood of passing ATS screening"

    def _get_company_notes(self, resume_data: Dict, profile: ATSProfile) -> List[str]:
        """Get company-specific notes and recommendations"""
        notes = []
        
        company_specific_advice = {
            'Amazon': ["Emphasize leadership principles", "Include system scalability metrics", 
                      "Highlight customer obsession examples"],
            'Google': ["Highlight algorithmic work", "Add research/publications if any", 
                      "Show innovation and impact metrics"],
            'Microsoft': ["Emphasize collaboration and teamwork", "Include cloud/Azure experience", 
                         "Show growth mindset examples"],
            'TCS': ["Show domain expertise", "Add client interaction experience", 
                   "Highlight delivery and project management"],
            'Infosys': ["Emphasize digital transformation projects", "Show consulting experience", 
                       "Add automation and innovation examples"],
            'Wipro': ["Highlight domain knowledge", "Show quality focus", 
                     "Add client delivery examples"],
            'IBM': ["Emphasize enterprise solutions", "Add AI/Watson experience", 
                   "Show consulting and transformation projects"],
            'Accenture': ["Highlight consulting experience", "Show strategy and transformation work", 
                         "Add client management examples"],
            'JP Morgan': ["Emphasize financial domain knowledge", "Add risk management experience", 
                         "Show analytical and quantitative skills"],
            'Goldman Sachs': ["Highlight investment and financial expertise", "Show analytical skills", 
                             "Add high-pressure environment experience"]
        }
        
        if profile.company in company_specific_advice:
            notes.extend(company_specific_advice[profile.company])
        else:
            notes.extend(["Focus on relevant keywords", "Highlight technical skills", 
                         "Show project experience"])
        
        return notes

    def _build_synonym_map(self) -> Dict[str, List[str]]:
        """Build a map of keywords to their synonyms for smart matching"""
        return {
            "machine learning": ["ml", "deep learning", "artificial intelligence", "ai"],
            "javascript": ["js", "node.js", "react", "angular", "vue"],
            "project management": ["pmp", "scrum master", "agile", "kanban"],
            "cloud computing": ["aws", "azure", "gcp", "google cloud", "cloud"],
            "ai": ["artificial intelligence", "machine learning", "ml", "neural networks"],
            "devops": ["ci/cd", "continuous integration", "continuous delivery", "docker", "kubernetes"],
            "database": ["sql", "mysql", "postgresql", "mongodb", "oracle"],
            "programming": ["coding", "development", "software engineering"],
            "leadership": ["management", "team lead", "supervisor", "director"],
            "analytics": ["data analysis", "business intelligence", "reporting", "metrics"]
        }

    def _initialize_ats_profiles(self) -> Dict[str, ATSProfile]:
        """Initialize ATS profiles for different companies"""
        return {
            'Amazon': ATSProfile(
                company='Amazon',
                keyword_weight=0.35, experience_weight=0.25,
                education_weight=0.15, skills_weight=0.20, format_weight=0.05,
                preferred_keywords={'aws', 'cloud', 'microservices', 'distributed systems', 'scalability',
                                   'leadership principles', 'customer obsession', 'ownership', 'bias for action',
                                   'java', 'python', 'sql', 'data structures', 'algorithms', 'system design'},
                required_skills={'programming', 'problem solving', 'system design', 'cloud computing', 'databases'},
                experience_requirements={'entry': 0, 'mid': 3, 'senior': 5, 'principal': 8},
                education_preferences=['bachelors', 'masters', 'phd'],
                scoring_strictness=0.8, common_filters=['leadership', 'innovation', 'scale']
            ),
            
            'Google': ATSProfile(
                company='Google',
                keyword_weight=0.30, experience_weight=0.25,
                education_weight=0.20, skills_weight=0.20, format_weight=0.05,
                preferred_keywords={'machine learning', 'ai', 'tensorflow', 'algorithms', 'data structures',
                                   'python', 'c++', 'java', 'go', 'distributed systems', 'gcp', 'research',
                                   'innovation', 'scalability', 'performance optimization'},
                required_skills={'programming', 'algorithms', 'data structures', 'system design', 'problem solving'},
                experience_requirements={'entry': 0, 'mid': 3, 'senior': 5, 'staff': 8},
                education_preferences=['masters', 'phd', 'bachelors'],
                scoring_strictness=0.85, common_filters=['innovation', 'research', 'impact']
            ),
            
            'Microsoft': ATSProfile(
                company='Microsoft',
                keyword_weight=0.32, experience_weight=0.28,
                education_weight=0.18, skills_weight=0.18, format_weight=0.04,
                preferred_keywords={'azure', 'c#', '.net', 'sql server', 'office 365', 'powershell', 'active directory',
                                   'sharepoint', 'teams', 'cloud computing', 'devops', 'agile'},
                required_skills={'programming', 'cloud platforms', 'collaboration', 'problem solving'},
                experience_requirements={'entry': 0, 'mid': 2, 'senior': 5, 'principal': 7},
                education_preferences=['bachelors', 'masters'],
                scoring_strictness=0.75, common_filters=['collaboration', 'diversity', 'growth mindset']
            ),
            
            'TCS': ATSProfile(
                company='TCS',
                keyword_weight=0.25, experience_weight=0.30,
                education_weight=0.25, skills_weight=0.15, format_weight=0.05,
                preferred_keywords={'java', 'spring', 'hibernate', 'sql', 'oracle', 'agile', 'scrum', 'banking', 'finance',
                                   'erp', 'sap', 'mainframe', 'cobol', 'testing', 'qa'},
                required_skills={'programming', 'database management', 'testing', 'domain knowledge'},
                experience_requirements={'entry': 0, 'mid': 3, 'senior': 6, 'lead': 8},
                education_preferences=['bachelors', 'masters'],
                scoring_strictness=0.70, common_filters=['domain expertise', 'client handling', 'delivery']
            ),
            
            'Infosys': ATSProfile(
                company='Infosys',
                keyword_weight=0.28, experience_weight=0.32,
                education_weight=0.22, skills_weight=0.15, format_weight=0.03,
                preferred_keywords={'java', 'python', 'sql', 'agile', 'devops', 'cloud', 'digital transformation',
                                   'automation', 'ai', 'machine learning', 'consulting'},
                required_skills={'programming', 'consulting', 'client interaction', 'problem solving'},
                experience_requirements={'entry': 0, 'mid': 2, 'senior': 5, 'principal': 8},
                education_preferences=['bachelors', 'masters'],
                scoring_strictness=0.72, common_filters=['innovation', 'digital', 'transformation']
            ),
            
            'Wipro': ATSProfile(
                company='Wipro',
                keyword_weight=0.26, experience_weight=0.30,
                education_weight=0.24, skills_weight=0.16, format_weight=0.04,
                preferred_keywords={'java', 'c++', 'sql', 'testing', 'automation', 'agile', 'healthcare', 'banking',
                                   'retail', 'cloud', 'devops', 'sap'},
                required_skills={'programming', 'domain knowledge', 'testing', 'project management'},
                experience_requirements={'entry': 0, 'mid': 3, 'senior': 5, 'manager': 7},
                education_preferences=['bachelors', 'masters'],
                scoring_strictness=0.68, common_filters=['domain expertise', 'quality', 'delivery']
            ),
            
            'IBM': ATSProfile(
                company='IBM',
                keyword_weight=0.30, experience_weight=0.25,
                education_weight=0.20, skills_weight=0.20, format_weight=0.05,
                preferred_keywords={'watson', 'ai', 'machine learning', 'cloud', 'blockchain', 'quantum', 'mainframe', 'db2',
                                   'websphere', 'consulting', 'transformation'},
                required_skills={'consulting', 'enterprise solutions', 'ai/ml', 'problem solving'},
                experience_requirements={'entry': 0, 'mid': 3, 'senior': 6, 'executive': 10},
                education_preferences=['masters', 'phd', 'bachelors'],
                scoring_strictness=0.78, common_filters=['innovation', 'research', 'enterprise']
            ),
            
            'Accenture': ATSProfile(
                company='Accenture',
                keyword_weight=0.27, experience_weight=0.28,
                education_weight=0.20, skills_weight=0.20, format_weight=0.05,
                preferred_keywords={'consulting', 'digital transformation', 'cloud', 'agile', 'change management',
                                   'strategy', 'analytics', 'ai', 'automation', 'client'},
                required_skills={'consulting', 'client management', 'strategy', 'digital transformation'},
                experience_requirements={'entry': 0, 'mid': 2, 'senior': 4, 'manager': 6},
                education_preferences=['masters', 'bachelors', 'mba'],
                scoring_strictness=0.75, common_filters=['consulting', 'strategy', 'transformation']
            ),
            
            'JP Morgan': ATSProfile(
                company='JP Morgan',
                keyword_weight=0.32, experience_weight=0.27,
                education_weight=0.20, skills_weight=0.18, format_weight=0.03,
                preferred_keywords={'finance', 'banking', 'risk', 'analytics', 'java', 'python', 'sql',
                                   'trading', 'investment', 'derivatives', 'portfolio'},
                required_skills={'finance', 'analytics', 'programming', 'risk management'},
                experience_requirements={'entry': 0, 'mid': 2, 'senior': 5, 'vp': 8},
                education_preferences=['masters', 'bachelors', 'mba'],
                scoring_strictness=0.77, common_filters=['finance', 'analytics', 'banking']
            ),
            
            'Goldman Sachs': ATSProfile(
                company='Goldman Sachs',
                keyword_weight=0.34, experience_weight=0.26,
                education_weight=0.20, skills_weight=0.17, format_weight=0.03,
                preferred_keywords={'finance', 'investment', 'banking', 'risk', 'analytics', 'java', 'python', 'sql',
                                   'trading', 'derivatives', 'fixed income', 'equity'},
                required_skills={'finance', 'analytics', 'programming', 'quantitative analysis'},
                experience_requirements={'entry': 0, 'mid': 3, 'senior': 6, 'md': 10},
                education_preferences=['masters', 'phd', 'mba'],
                scoring_strictness=0.80, common_filters=['finance', 'investment', 'analytics']
            ),
            
            'Generic': ATSProfile(
                company='Generic',
                keyword_weight=0.30, experience_weight=0.25,
                education_weight=0.20, skills_weight=0.20, format_weight=0.05,
                preferred_keywords={'programming', 'problem solving', 'teamwork', 'communication', 
                                   'leadership', 'project management'},
                required_skills={'programming', 'problem solving', 'communication'},
                experience_requirements={'entry': 0, 'mid': 3, 'senior': 5},
                education_preferences=['bachelors', 'masters'],
                scoring_strictness=0.70, common_filters=['skills', 'experience', 'education']
            )
        }


    def quick_simulate(self, resume_data: Dict, company: str = None, mode: str = None) -> Dict:
        """
        Quick simulation with automatic defaults - handles missing parameters gracefully
        
        Args:
            resume_data (Dict): Resume data to analyze
            company (str, optional): Company name. If None, will prompt user.
            mode (str, optional): Scoring mode. If None, will prompt user.
        
        Returns:
            Dict: ATS scoring results
        """
        try:
            # Handle missing company
            if company is None:
                print("\n📋 Company not specified. Please select:")
                company = self.choose_company()
            
            # Handle missing mode
            if mode is None:
                print("\n⚙️ Mode not specified. Please select:")
                mode = self.choose_scoring_mode()
            
            # Run simulation
            return self.simulate_ats_filtering(resume_data, company, mode)
            
        except Exception as e:
            print(f"❌ Error in ATS simulation: {str(e)}")
            print("🔄 Using default settings (Generic company, rule-based mode)")
            return self.simulate_ats_filtering(resume_data, "Generic", "rule")
    
    def simple_score(self, resume_text: str, company: str = "Generic") -> float:
        """
        Simplified scoring method that only needs resume text
        
        Args:
            resume_text (str): Raw resume text
            company (str): Company name (default: Generic)
        
        Returns:
            float: Overall ATS score (0-100)
        """
        # Convert text to basic resume data structure
        resume_data = {
            'contact_info': {'email': 'placeholder@email.com'},
            'raw_text': resume_text,
            'skills': self._extract_skills_from_text(resume_text),
            'experience_years': self._estimate_experience_years(resume_text),
            'education_level': self._detect_education_level(resume_text),
            'sections': self._detect_sections(resume_text)
        }
        
        # Run simulation with default rule-based mode
        results = self.simulate_ats_filtering(resume_data, company, "rule")
        return results['overall_ats_score']
        """
        Main method to run complete ATS simulation with user interaction
        """
        print("=== Welcome to ATS Simulation System ===")
        
        # Use sample data if none provided
        if resume_data is None:
            resume_data = self.get_sample_resume_data()
        
        # Get user choices
        mode = self.choose_scoring_mode()
        company = self.choose_company()
        
        print(f"\nRunning ATS simulation for {company} using {mode} mode...")
        print("-" * 50)
        
        # Run simulation
        results = self.simulate_ats_filtering(resume_data, company, mode)
        
        # Display results
        self.display_results(results, company, mode)
        
        return results
    
    def get_sample_resume_data(self) -> Dict:
        """Get sample resume data for testing"""
        return {
            'contact_info': {'email': 'test@example.com'},
            'raw_text': 'Software Engineer with 5 years experience in Java, Python, AWS cloud computing, machine learning, and system design. Led teams and delivered scalable solutions. Experience with agile methodologies, microservices architecture, and database management.',
            'skills': ['Java', 'Python', 'AWS', 'Machine Learning', 'System Design', 'Microservices', 'Agile'],
            'experience_years': 5,
            'education_level': 'bachelors',
            'sections': {'experience': True, 'education': True, 'skills': True, 'summary': True}
        }
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract likely skills from resume text"""
        common_skills = [
            'python', 'java', 'javascript', 'c++', 'sql', 'html', 'css', 'react', 'angular',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'linux', 'mongodb',
            'machine learning', 'ai', 'data science', 'analytics', 'project management',
            'agile', 'scrum', 'devops', 'testing', 'automation', 'cloud computing'
        ]
        
        text_lower = text.lower()
        found_skills = [skill for skill in common_skills if skill in text_lower]
        return found_skills[:10]  # Limit to top 10 matches
    
    def _estimate_experience_years(self, text: str) -> int:
        """Estimate years of experience from resume text"""
        import re
        
        # Look for patterns like "5 years", "3+ years", etc.
        year_patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'(\d+)\+?\s*years?\s+in',
            r'experience.*?(\d+)\+?\s*years?',
        ]
        
        years = []
        for pattern in year_patterns:
            matches = re.findall(pattern, text.lower())
            years.extend([int(match) for match in matches])
        
        return max(years) if years else 2  # Default to 2 years
    
    def _detect_education_level(self, text: str) -> str:
        """Detect education level from resume text"""
        text_lower = text.lower()
        
        if any(term in text_lower for term in ['phd', 'ph.d', 'doctorate', 'doctoral']):
            return 'phd'
        elif any(term in text_lower for term in ['masters', 'master', 'mba', 'm.s', 'm.a']):
            return 'masters'
        elif any(term in text_lower for term in ['bachelor', 'b.s', 'b.a', 'b.tech', 'b.e']):
            return 'bachelors'
        else:
            return 'bachelors'  # Default assumption
    
    def _detect_sections(self, text: str) -> Dict[str, bool]:
        """Detect which sections are present in resume"""
        text_lower = text.lower()
        
        sections = {}
        section_keywords = {
            'experience': ['experience', 'work history', 'employment', 'professional'],
            'education': ['education', 'academic', 'university', 'college', 'degree'],
            'skills': ['skills', 'technical skills', 'competencies', 'proficiencies'],
            'summary': ['summary', 'objective', 'profile', 'about']
        }
        
        for section, keywords in section_keywords.items():
            sections[section] = any(keyword in text_lower for keyword in keywords)
        
        return sections

    def run_ats_simulation(self, resume_data: Dict = None) -> Dict:
        """Display ATS simulation results in a formatted way"""
        print(f"\n🏢 COMPANY: {company}")
        print(f"🔧 MODE: {mode.upper()}")
        print("=" * 60)
        
        print(f"📊 OVERALL ATS SCORE: {results['overall_ats_score']}/100")
        print(f"✅ PASSES INITIAL SCREENING: {'YES' if results['passes_initial_screening'] else 'NO'}")
        print(f"📝 RECOMMENDATION: {results['ats_recommendation']}")
        
        print("\n📈 DETAILED SCORES:")
        print(f"   • Keyword Score: {results['keyword_score']}/100")
        print(f"   • Experience Score: {results['experience_score']}/100")
        print(f"   • Education Score: {results['education_score']}/100")
        print(f"   • Skills Score: {results['skills_score']}/100")
        print(f"   • Format Score: {results['format_score']}/100")
        
        if results['company_specific_notes']:
            print(f"\n💡 COMPANY-SPECIFIC RECOMMENDATIONS:")
            for note in results['company_specific_notes']:
                print(f"   • {note}")
        
        print("\n" + "=" * 60)


# Example usage and testing functions
def test_specific_company(company_name: str = "Amazon", mode: str = "smart"):
    """Test ATS simulation for a specific company and mode"""
    ats = CompanyATS()
    
    sample_resume = {
        'contact_info': {'email': 'john.doe@example.com'},
        'raw_text': '''Senior Software Engineer with 8 years of experience in distributed systems, 
        cloud computing, and machine learning. Proficient in Java, Python, AWS, microservices architecture.
        Led multiple teams and delivered scalable solutions serving millions of customers. Experience with
        system design, algorithms, data structures, and performance optimization. Strong background in
        leadership principles and customer obsession.''',
        'skills': ['Java', 'Python', 'AWS', 'Machine Learning', 'System Design', 'Microservices', 
                  'Leadership', 'Algorithms', 'Data Structures'],
        'experience_years': 8,
        'education_level': 'masters',
        'sections': {'experience': True, 'education': True, 'skills': True, 'summary': True}
    }
    
    print(f"=== Testing {company_name} - {mode.upper()} Mode ===")
    results = ats.simulate_ats_filtering(sample_resume, company_name, mode)
    ats.display_results(results, company_name, mode)
    return results

def compare_modes(company_name: str = "Google"):
    """Compare rule-based vs smart mode for the same company"""
    ats = CompanyATS()
    
    sample_resume = {
        'contact_info': {'email': 'alice.smith@example.com'},
        'raw_text': '''Data Scientist with 6 years of experience in machine learning, artificial intelligence,
        and big data analytics. Expert in Python, TensorFlow, algorithms, and statistical modeling.
        Published research papers and contributed to open-source ML projects. Experience with distributed
        systems, cloud platforms (GCP), and performance optimization.''',
        'skills': ['Python', 'Machine Learning', 'TensorFlow', 'Algorithms', 'Statistics', 
                  'Research', 'GCP', 'Data Analysis'],
        'experience_years': 6,
        'education_level': 'phd',
        'sections': {'experience': True, 'education': True, 'skills': True, 'summary': True}
    }
    
    print(f"=== COMPARING MODES FOR {company_name} ===")
    
    # Test rule-based
    rule_results = ats.simulate_ats_filtering(sample_resume, company_name, 'rule')
    print("\n🔧 RULE-BASED MODE:")
    print(f"Overall Score: {rule_results['overall_ats_score']}/100")
    
    # Test smart mode
    smart_results = ats.simulate_ats_filtering(sample_resume, company_name, 'smart')
    print("\n🧠 SMART MODE:")
    print(f"Overall Score: {smart_results['overall_ats_score']}/100")
    
    print(f"\n📊 SCORE DIFFERENCE: {abs(smart_results['overall_ats_score'] - rule_results['overall_ats_score']):.2f} points")

def interactive_demo():
    """Run interactive demo of the ATS system"""
    ats = CompanyATS()
    
    print("🚀 Starting Interactive ATS Simulation Demo...")
    print("\nUsing sample resume data for demonstration.")
    
    # Run the full interactive simulation
    results = ats.run_ats_simulation()
    
    # Ask if user wants to try another combination
    while True:
        try_again = input("\n❓ Would you like to try another company/mode? (y/n): ").strip().lower()
        if try_again == 'y':
            results = ats.run_ats_simulation()
        else:
            print("👋 Thanks for using ATS Simulation System!")
            break

# ==================== ERROR HANDLING & DEBUGGING ====================

def debug_ats_call():
    """Debug function to test ATS calls and identify issues"""
    print("🔍 ATS DEBUG MODE")
    print("=" * 50)
    
    # Test 1: Basic instantiation
    try:
        ats = CompanyATS()
        print("✅ ATS instantiation: SUCCESS")
    except Exception as e:
        print(f"❌ ATS instantiation: FAILED - {e}")
        return
    
    # Test 2: Sample data creation
    try:
        sample_data = {
            'contact_info': {'email': 'test@example.com'},
            'raw_text': 'Software Engineer with 3 years experience in Python, Java, and cloud computing.',
            'skills': ['Python', 'Java', 'Cloud Computing'],
            'experience_years': 3,
            'education_level': 'bachelors',
            'sections': {'experience': True, 'education': True, 'skills': True}
        }
        print("✅ Sample data creation: SUCCESS")
    except Exception as e:
        print(f"❌ Sample data creation: FAILED - {e}")
        return
    
    # Test 3: Method calls with all parameters
    try:
        result1 = ats.simulate_ats_filtering(sample_data, "Amazon", "rule")
        print("✅ Full parameter call: SUCCESS")
        print(f"   Score: {result1['overall_ats_score']}")
    except Exception as e:
        print(f"❌ Full parameter call: FAILED - {e}")
    
    # Test 4: Method calls with default parameters
    try:
        result2 = ats.simulate_ats_filtering(sample_data)
        print("✅ Default parameter call: SUCCESS")
        print(f"   Score: {result2['overall_ats_score']}")
    except Exception as e:
        print(f"❌ Default parameter call: FAILED - {e}")
    
    # Test 5: Quick simulate method
    try:
        result3 = ats.quick_simulate(sample_data, "Google", "smart")
        print("✅ Quick simulate call: SUCCESS")
        print(f"   Score: {result3['overall_ats_score']}")
    except Exception as e:
        print(f"❌ Quick simulate call: FAILED - {e}")
    
    # Test 6: Simple score method
    try:
        score = ats.simple_score("I am a software engineer with Python and Java experience.")
        print("✅ Simple score call: SUCCESS")
        print(f"   Score: {score}")
    except Exception as e:
        print(f"❌ Simple score call: FAILED - {e}")
    
    print("\n🎯 All tests completed!")

def safe_ats_call(resume_data, company=None, mode=None):
    """
    Completely safe ATS call that handles all errors gracefully
    
    Args:
        resume_data: Resume data (dict or string)
        company: Company name (optional)
        mode: Scoring mode (optional)
    
    Returns:
        Dict: ATS results or error information
    """
    try:
        ats = CompanyATS()
        
        # Handle string input (convert to dict)
        if isinstance(resume_data, str):
            resume_data = {
                'contact_info': {'email': 'placeholder@email.com'},
                'raw_text': resume_data,
                'skills': ats._extract_skills_from_text(resume_data),
                'experience_years': ats._estimate_experience_years(resume_data),
                'education_level': ats._detect_education_level(resume_data),
                'sections': ats._detect_sections(resume_data)
            }
        
        # Use quick_simulate for best error handling
        return ats.quick_simulate(resume_data, company, mode)
        
    except Exception as e:
        return {
            'error': True,
            'message': f"ATS simulation failed: {str(e)}",
            'overall_ats_score': 0,
            'passes_initial_screening': False,
            'ats_recommendation': 'Unable to process resume'
        }


# ==================== EASY USAGE FUNCTIONS ====================

def easy_ats_score(resume_text: str, company: str = "Generic") -> float:
    """
    Easiest way to get ATS score - just pass resume text
    
    Args:
        resume_text (str): Resume content as string
        company (str): Company name (default: Generic)
    
    Returns:
        float: ATS score from 0-100
    """
    result = safe_ats_call(resume_text, company, "rule")
    return result.get('overall_ats_score', 0)

def compare_companies(resume_text: str, companies: List[str] = None) -> Dict[str, float]:
    """
    Compare ATS scores across multiple companies
    
    Args:
        resume_text (str): Resume content
        companies (List[str]): List of companies to compare (optional)
    
    Returns:
        Dict[str, float]: Company names mapped to ATS scores
    """
    if companies is None:
        companies = ["Amazon", "Google", "Microsoft", "Generic"]
    
    results = {}
    for company in companies:
        try:
            score = easy_ats_score(resume_text, company)
            results[company] = score
        except:
            results[company] = 0
    
    return results


# Example usage and testing functions
def test_all_error_cases():
    """Test all possible error scenarios"""
    print("🧪 TESTING ALL ERROR CASES")
    print("=" * 50)
    
    # Test with missing arguments
    try:
        ats = CompanyATS()
        # This should now work with default parameters
        result = ats.simulate_ats_filtering({
            'raw_text': 'test',
            'skills': [],
            'contact_info': {'email': 'test@test.com'}
        })
        print("✅ Missing arguments handled successfully")
    except Exception as e:
        print(f"❌ Missing arguments test failed: {e}")
    
    # Test with invalid data
    try:
        result = safe_ats_call("Just a simple resume text")
        print("✅ String input handled successfully")
        print(f"   Score: {result['overall_ats_score']}")
    except Exception as e:
        print(f"❌ String input test failed: {e}")
    
    # Test easy function
    try:
        score = easy_ats_score("Software engineer with Python and Java skills")
        print(f"✅ Easy ATS score: {score}")
    except Exception as e:
        print(f"❌ Easy ATS score failed: {e}")
    
    # Test comparison
    try:
        comparison = compare_companies("Data scientist with machine learning experience")
        print("✅ Company comparison successful:")
        for company, score in comparison.items():
            print(f"   {company}: {score}")
    except Exception as e:
        print(f"❌ Company comparison failed: {e}")


def main():
    """Main function with multiple options to avoid errors"""
    print("🎯 ATS SIMULATION SYSTEM")
    print("=" * 50)
    
    print("\n🔍 Running debug tests first...")
    debug_ats_call()
    
    print("\n🧪 Testing error handling...")
    test_all_error_cases()
    
    print("\n📊 Quick example:")
    try:
        # This should always work
        score = easy_ats_score("Senior Software Engineer with 5+ years experience in Python, Java, AWS, and machine learning")
        print(f"✅ Sample ATS Score: {score}/100")
        
        # Compare across companies
        comparison = compare_companies("Data scientist with PhD and machine learning expertise", ["Google", "Amazon", "Microsoft"])
        print("\n🏢 Company Comparison:")
        for company, score in sorted(comparison.items(), key=lambda x: x[1], reverse=True):
            print(f"   {company}: {score}/100")
            
    except Exception as e:
        print(f"❌ Even the safe functions failed: {e}")
        print("Please check if there are conflicts with other modules.")


if __name__ == "__main__":
    main()