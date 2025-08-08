#!/usr/bin/env python3
"""
RESUIN - Optimized Resume Analyzer Main Application
Enhanced to work with improved ResumeAnalyzer and CompanyATS modules
"""

import os
import sys
import json
from typing import Optional, Dict
from modules.resume_parser import ResumeParser
from modules.company_ats import CompanyATS
from modules.analyzer import ResumeAnalyzer, AnalysisResult
from modules.report_generator import ReportGenerator

class RESUIN:
    def __init__(self):
        self.parser = ResumeParser()
        self.analyzer = ResumeAnalyzer()
        self.report_generator = ReportGenerator()
        self.company_ats = self.analyzer.company_ats  # Use the analyzer's ATS instance
        
    def display_welcome(self) -> None:
        """Display welcome message with enhanced information"""
        print("=" * 60)
        print("🎯 RESUIN - Advanced Resume Analyzer (Optimized)")
        print("=" * 60)
        print("Analyzes resumes against company-specific ATS systems")
        print("Now with improved scoring algorithms and recommendations")
        print("Supports both rule-based and smart (ML-simulated) modes\n")
        
    def get_resume_file(self) -> str:
        """Get resume file path from user with improved validation"""
        while True:
            file_path = input("📄 Enter resume file path (PDF/DOCX/TXT/JSON): ").strip()
            
            if not file_path:
                print("❌ Please enter a valid file path")
                continue
                
            if not os.path.exists(file_path):
                print("❌ File not found. Please check the path and try again")
                continue
                
            if file_path.lower().endswith('.json'):
                return file_path
                
            if not file_path.lower().endswith(('.pdf', '.docx', '.doc', '.txt')):
                print("❌ Please provide a PDF, DOCX, TXT, or JSON file")
                continue
                
            return file_path
            
    def get_company_selection(self) -> str:
        """Get target company from user with scoring mode selection"""
        companies = self.company_ats.get_available_companies()
        
        print("\n🏢 Select target company:")
        for i, company in enumerate(companies, 1):
            print(f"{i}. {company}")
        print(f"{len(companies)+1}. Compare across all companies")
            
        while True:
            try:
                choice = int(input(f"\nEnter choice (1-{len(companies)+1}): "))
                if 1 <= choice <= len(companies):
                    return companies[choice - 1]
                elif choice == len(companies)+1:
                    return "compare_all"
                else:
                    print(f"❌ Please enter a number between 1 and {len(companies)+1}")
            except ValueError:
                print("❌ Please enter a valid number")
                
    def get_scoring_mode(self) -> str:
        """Get scoring mode from user"""
        while True:
            print("\n🔢 Select scoring mode:")
            print("1. Rule-based (faster, basic matching)")
            print("2. Smart mode (slower, advanced ML-simulated matching)")
            choice = input("Enter choice (1-2): ").strip()
            
            if choice == "1":
                return "rule"
            elif choice == "2":
                return "smart"
            else:
                print("❌ Please enter 1 or 2")
                
    def get_job_description(self) -> Optional[str]:
        """Get job description from user with improved input handling"""
        print("\n📋 Optional: Paste job description (press Enter twice when done):")
        print("(Leave blank if not available)")
        
        lines = []
        empty_lines = 0
        
        while empty_lines < 2:
            try:
                line = input()
                if line.strip() == "":
                    empty_lines += 1
                else:
                    empty_lines = 0
                    lines.append(line)
            except EOFError:
                break
                
        job_description = "\n".join(lines).strip()
        return job_description if job_description else None
        
    def load_resume_data(self, file_path: str) -> Dict:
        """Load resume data from file with improved error handling"""
        try:
            if file_path.lower().endswith('.json'):
                with open(file_path, 'r') as f:
                    return json.load(f)
            else:
                return self.parser.parse_resume(file_path)
        except Exception as e:
            print(f"❌ Error loading resume: {str(e)}")
            raise ValueError("Failed to load resume data")
            
    def run_comparison_analysis(self, resume_data: Dict, job_description: Optional[str] = None) -> Dict[str, AnalysisResult]:
        """Run analysis across all companies"""
        companies = self.company_ats.get_available_companies()
        results = {}
        
        print("\n🔍 Running comparison across all companies...")
        for company in companies:
            print(f"  Analyzing for {company}...", end='\r')
            try:
                results[company] = self.analyzer.analyze_resume(
                    resume_data=resume_data,
                    company=company,
                    job_description=job_description,
                    mode="rule"  # Use rule-based for faster comparison
                )
            except Exception as e:
                print(f"  ❌ Error analyzing for {company}: {str(e)}")
                continue
                
        return results
        
    def run_analysis(self) -> None:
        """Main application flow with enhanced error handling"""
        try:
            self.display_welcome()
            
            # Step 1: Get resume file
            resume_file = self.get_resume_file()
            print(f"✅ Resume file loaded: {os.path.basename(resume_file)}")
            
            # Step 2: Load resume data
            print("\n🔍 Loading resume data...")
            try:
                resume_data = self.load_resume_data(resume_file)
                if not resume_data:
                    raise ValueError("No resume data extracted")
                print("✅ Resume data loaded successfully")
            except Exception as e:
                print(f"❌ Failed to load resume data: {str(e)}")
                return
                
            # Step 3: Get scoring mode
            mode = self.get_scoring_mode()
            print(f"✅ Selected mode: {'Smart' if mode == 'smart' else 'Rule-based'}")
            
            # Step 4: Get job description
            job_description = self.get_job_description()
            if job_description:
                print("✅ Job description added")
                
            # Step 5: Select company or comparison
            company = self.get_company_selection()
            
            if company == "compare_all":
                # Run comparison across all companies
                results = self.run_comparison_analysis(resume_data, job_description)
                if not results:
                    print("❌ No analysis results generated")
                    return
                    
                print("\n📊 Comparison Results:")
                self.report_generator.display_comparison(results)
                
                # Save report
                save_option = input("\n💾 Save comparison report? (y/n): ").strip().lower()
                if save_option == 'y':
                    filename = "resuin_comparison_report.txt"
                    self.report_generator.save_comparison(results, filename)
                    print(f"✅ Report saved as: {filename}")
            else:
                # Single company analysis
                print(f"✅ Target company: {company}")
                
                # Step 6: Run analysis
                print(f"\n🤖 Analyzing resume for {company} ({'smart' if mode == 'smart' else 'rule-based'} mode)...")
                
                analysis_result = self.analyzer.analyze_resume(
                    resume_data=resume_data,
                    company=company,
                    job_description=job_description,
                    mode=mode
                )
                
                # Step 7: Generate and display report
                print("\n📊 Generating detailed report...\n")
                self.report_generator.display_report(analysis_result)
                
                # Step 8: Save report option
                save_option = input("\n💾 Save report to file? (y/n): ").strip().lower()
                if save_option == 'y':
                    filename = f"resuin_analysis_{company.lower().replace(' ', '_')}.txt"
                    self.report_generator.save_report(analysis_result, filename)
                    print(f"✅ Report saved as: {filename}")
                    
        except KeyboardInterrupt:
            print("\n\n👋 Analysis cancelled by user")
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {str(e)}")
            if "resume" in str(e).lower():
                print("Please check your resume file and try again")
            else:
                print("Please try again or contact support")

def main():
    """Entry point of the application"""
    try:
        resuin = RESUIN()
        resuin.run_analysis()
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()