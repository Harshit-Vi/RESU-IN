"""
Report Generator Module
Generates detailed analysis reports and displays results
"""

from typing import Dict, List
import datetime
import sys
import dataclasses

class ReportGenerator:
    def __init__(self):
        self.report_template = self._load_report_template()
    
    def display_report(self, analysis_result):
        """Display comprehensive analysis report"""
        # Ensure analysis_result is a dict
        if dataclasses.is_dataclass(analysis_result):
            analysis_result = dataclasses.asdict(analysis_result)

        self._print_header(analysis_result)
        self._print_overall_score(analysis_result)
        self._print_ats_analysis(analysis_result)
        self._print_section_analysis(analysis_result)
        self._print_keyword_analysis(analysis_result)
        self._print_recommendations(analysis_result)
        self._print_footer()
    
    def save_report(self, analysis_result, filename: str):
        """Save report to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                original_stdout = sys.stdout
                sys.stdout = f
                self.display_report(analysis_result)
                sys.stdout = original_stdout
        except Exception as e:
            print(f"Error saving report: {str(e)}")
    
    def _print_header(self, analysis_result: Dict):
        """Print report header"""
        print("=" * 80)
        print("🎯 RESUIN - RESUME ANALYSIS REPORT")
        print("=" * 80)
        print(f"📅 Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🏢 Target Company: {analysis_result['company']}")
        print(f"📄 Resume Summary: {self._format_resume_summary(analysis_result['resume_summary'])}")
        print("=" * 80)
    
    def _print_overall_score(self, analysis_result: Dict):
        """Print overall score section"""
        score = analysis_result['overall_score']
        print(f"\n🏆 OVERALL RESUME SCORE: {score}/100")
        print(self._get_score_bar(score))
        print(f"📈 Assessment: {self._get_score_assessment(score)}")
        print("-" * 60)
    
    def _print_ats_analysis(self, analysis_result: Dict):
        """Print ATS analysis section"""
        ats = analysis_result['ats_results']
        
        print("\n🤖 ATS SIMULATION RESULTS")
        print("=" * 40)
        print(f"✅ Initial Screening: {'PASS' if ats['passes_initial_screening'] else 'FAIL'}")
        print(f"📊 ATS Score: {ats['overall_ats_score']:.1f}/100")
        print(f"🎯 Recommendation: {ats['ats_recommendation']}")
        
        print("\n📋 Detailed ATS Breakdown:")
        print(f"  • Keywords:    {ats['keyword_score']:.1f}/100 {self._get_mini_bar(ats['keyword_score'])}")
        print(f"  • Experience:  {ats['experience_score']:.1f}/100 {self._get_mini_bar(ats['experience_score'])}")
        print(f"  • Education:   {ats['education_score']:.1f}/100 {self._get_mini_bar(ats['education_score'])}")
        print(f"  • Skills:      {ats['skills_score']:.1f}/100 {self._get_mini_bar(ats['skills_score'])}")
        print(f"  • Format:      {ats['format_score']:.1f}/100 {self._get_mini_bar(ats['format_score'])}")
        
        if ats.get('company_specific_notes'):
            print(f"\n🏢 {analysis_result['company']}-Specific Notes:")
            for note in ats['company_specific_notes']:
                print(f"  • {note}")
        
        print("-" * 60)
    
    def _print_section_analysis(self, analysis_result: Dict):
        """Print section-by-section analysis"""
        sections = analysis_result['section_analysis']
        
        print("\n📑 SECTION-BY-SECTION ANALYSIS")
        print("=" * 40)
        
        for section_name, data in sections.items():
            status = "✅" if data['present'] else "❌"
            strength_emoji = self._get_strength_emoji(data['strength'])
            
            print(f"\n{status} {section_name.upper()} {strength_emoji}")
            print(f"   Status: {'Present' if data['present'] else 'Missing'}")
            if data['present']:
                print(f"   Strength: {data['strength']}")
                print(f"   Word Count: {data['word_count']}")
            
            if data.get('suggestions'):
                print("   💡 Suggestions:")
                for suggestion in data['suggestions']:
                    print(f"      • {suggestion}")
        
        print("-" * 60)
    
    def _print_keyword_analysis(self, analysis_result: Dict):
        """Print keyword analysis"""
        gaps = analysis_result['keyword_gaps']
        
        print("\n🔍 KEYWORD ANALYSIS")
        print("=" * 40)
        
        print(f"📈 Company Keyword Match: {gaps['keyword_match_percentage']:.1f}%")
        print(self._get_score_bar(gaps['keyword_match_percentage']))
        
        if gaps.get('jd_skill_match_percentage'):
            print(f"📈 Job Description Match: {gaps['jd_skill_match_percentage']:.1f}%")
            print(self._get_score_bar(gaps['jd_skill_match_percentage']))
        
        if gaps['matched_company_keywords']:
            print(f"\n✅ Found Keywords ({len(gaps['matched_company_keywords'])}):")
            self._print_keyword_list(gaps['matched_company_keywords'])
        
        if gaps['missing_company_keywords']:
            print(f"\n❌ Missing Keywords ({len(gaps['missing_company_keywords'])}):")
            self._print_keyword_list(gaps['missing_company_keywords'])
        
        if gaps.get('missing_jd_skills'):
            print(f"\n🎯 Missing Job-Specific Skills ({len(gaps['missing_jd_skills'])}):")
            self._print_keyword_list(gaps['missing_jd_skills'])
        
        print("-" * 60)
    
    def _print_recommendations(self, analysis_result: Dict):
        """Print recommendations section"""
        recommendations = analysis_result['recommendations']
        
        print("\n💡 IMPROVEMENT RECOMMENDATIONS")
        print("=" * 40)
        
        high_priority = [r for r in recommendations if r['priority'] == 'High']
        medium_priority = [r for r in recommendations if r['priority'] == 'Medium']
        low_priority = [r for r in recommendations if r['priority'] == 'Low']
        
        for priority, recs in [('HIGH PRIORITY', high_priority), 
                              ('MEDIUM PRIORITY', medium_priority),
                              ('LOW PRIORITY', low_priority)]:
            if recs:
                print(f"\n🚨 {priority}")
                for i, rec in enumerate(recs, 1):
                    print(f"\n{i}. {rec['title']} [{rec['category']}]")
                    print(f"   📝 {rec['description']}")
                    print("   🎯 Action Items:")
                    for action in rec['action_items']:
                        print(f"      • {action}")
        
        print("-" * 60)
    
    def _print_footer(self):
        """Print report footer"""
        print("\n" + "=" * 80)
        print("🎯 RESUIN Analysis Complete")
        print("💡 Implement the recommendations to improve your resume score")
        print("🚀 Good luck with your job application!")
        print("=" * 80)
    
    def _format_resume_summary(self, summary: Dict) -> str:
        return (f"{summary['total_experience']} years exp, "
                f"{summary['skill_count']} skills, "
                f"{summary['section_count']} sections")
    
    def _get_score_assessment(self, score: int) -> str:
        if score >= 85:
            return "Excellent - Strong chance of success"
        elif score >= 75:
            return "Good - Above average resume"
        elif score >= 65:
            return "Fair - Needs some improvements"
        elif score >= 50:
            return "Poor - Requires significant improvements"
        else:
            return "Critical - Major overhaul needed"
    
    def _get_score_bar(self, score: float) -> str:
        bar_length = 30
        filled_length = int(bar_length * score / 100)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        return f"[{bar}] {score:.1f}%"
    
    def _get_mini_bar(self, score: float) -> str:
        bar_length = 10
        filled_length = int(bar_length * score / 100)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        return f"[{bar}]"
    
    def _get_strength_emoji(self, strength: str) -> str:
        emoji_map = {
            'Excellent': '🌟',
            'Good': '✅',
            'Fair': '⚠️',
            'Poor': '❌'
        }
        return emoji_map.get(strength, '❓')
    
    def _print_keyword_list(self, keywords: List[str]):
        if not keywords:
            return
        cols = 3
        for i in range(0, len(keywords), cols):
            row = keywords[i:i+cols]
            formatted_row = [f"{word:<20}" for word in row]
            print("   " + "".join(formatted_row))
    
    def _load_report_template(self) -> str:
        return ""
