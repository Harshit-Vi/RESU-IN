#!/usr/bin/env python3
"""
RESUIN - Resume Analyzer Main Application
A comprehensive resume analysis tool that simulates company-specific ATS behavior
"""

import os
import sys
import dataclasses
from typing import Optional
from modules.resume_parser import ResumeParser
from modules.company_ats import CompanyATS
from modules.analyzer import ResumeAnalyzer
from modules.report_generator import ReportGenerator


class RESUIN:
    def __init__(self):
        self.parser = ResumeParser()
        self.company_ats = CompanyATS()
        self.analyzer = ResumeAnalyzer()
        self.report_generator = ReportGenerator()
        
    def display_welcome(self):
        """Display welcome message and application info"""
        print("=" * 60)
        print("🎯 RESUIN - Advanced Resume Analyzer")
        print("=" * 60)
        print("Analyzes resumes against company-specific ATS systems")
        print("Provides detailed scoring and improvement recommendations")
        print("Simulates ATS behavior with 80%+ accuracy\n")

    def get_resume_file(self) -> str:
        """Get resume file path from user"""
        while True:
            file_path = input("📄 Enter resume file path (PDF/DOCX): ").strip()
            if not file_path:
                print("❌ Please enter a valid file path")
                continue
            if not os.path.exists(file_path):
                print("❌ File not found. Please check the path and try again")
                continue
            if not file_path.lower().endswith(('.pdf', '.docx', '.doc')):
                print("❌ Please provide a PDF or DOCX file")
                continue
            return file_path

    def get_company_selection(self) -> str:
        """Get target company from user"""
        companies = self.company_ats.get_available_companies()
        print("\n🏢 Select target company:")
        for i, company in enumerate(companies, 1):
            print(f"{i}. {company}")
        while True:
            try:
                choice = int(input(f"\nEnter choice (1-{len(companies)}): "))
                if 1 <= choice <= len(companies):
                    return companies[choice - 1]
                else:
                    print(f"❌ Please enter a number between 1 and {len(companies)}")
            except ValueError:
                print("❌ Please enter a valid number")

    def get_analysis_mode(self) -> str:
        """Let user choose ATS analysis mode."""
        print("\n⚙️  Select ATS analysis mode:")
        print("1. Rule-based (faster, fixed keyword matching)")
        print("2. Smart analysis (slower, weighted scoring)")
        while True:
            choice = input("Enter choice (1-2): ").strip()
            if choice == "1":
                return "rule"
            elif choice == "2":
                return "smart"
            else:
                print("❌ Please enter 1 or 2")

    def get_job_description(self) -> Optional[str]:
        """Get job description from user"""
        print("\n📋 Job Description:")
        print("Paste the job description below (press Enter twice when done):")
        lines = []
        empty_lines = 0
        while empty_lines < 2:
            line = input()
            if line.strip() == "":
                empty_lines += 1
            else:
                empty_lines = 0
            lines.append(line)
        job_description = "\n".join(lines).strip()
        return job_description if job_description else None

    def run_analysis(self):
        """Main application flow"""
        try:
            self.display_welcome()

            resume_file = self.get_resume_file()
            print(f"✅ Resume file loaded: {os.path.basename(resume_file)}")

            print("\n🔍 Parsing resume...")
            resume_data = self.parser.parse_resume(resume_file)
            if not resume_data:
                print("❌ Failed to parse resume. Please check the file format.")
                return
            print("✅ Resume parsed successfully")

            company = self.get_company_selection()
            print(f"✅ Target company: {company}")

            mode = self.get_analysis_mode()
            print(f"✅ Selected ATS mode: {mode}")

            job_description = self.get_job_description()
            if job_description:
                print("✅ Job description added")

            print(f"\n🤖 Analyzing resume for {company} ATS ({mode} mode)...")
            print("This may take a few moments...")

            analysis_result = self.analyzer.analyze_resume(
                resume_data=resume_data,
                company=company,
                job_description=job_description,
                mode=mode
            )

            if dataclasses.is_dataclass(analysis_result):
                analysis_result = dataclasses.asdict(analysis_result)

            print("\n📊 Generating detailed report...\n")
            self.report_generator.display_report(analysis_result)

            save_option = input("\n💾 Save report to file? (y/n): ").strip().lower()
            if save_option == 'y':
                filename = f"resuin_analysis_{company.lower().replace(' ', '_')}.txt"
                self.report_generator.save_report(analysis_result, filename)
                print(f"✅ Report saved as: {filename}")

        except KeyboardInterrupt:
            print("\n\n👋 Analysis cancelled by user")
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            print("Please check your inputs and try again")


def main():
    resuin = RESUIN()
    resuin.run_analysis()


if __name__ == "__main__":
    main()
