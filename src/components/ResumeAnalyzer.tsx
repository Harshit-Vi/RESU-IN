import { useState } from 'react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { FileUpload } from "./FileUpload";
import { CompanySelector } from "./CompanySelector";
import { JobDescriptionUpload } from "./JobDescriptionUpload";
import { AnalysisResults } from "./AnalysisResults";
import { CheckCircle, Clock, Upload, Target, FileText, Brain, ArrowLeft } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface Company {
  id: string;
  name: string;
  atsType: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  industry: string;
  description: string;
}

interface Step {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  completed: boolean;
}

export const ResumeAnalyzer = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);
  const [jobDescription, setJobDescription] = useState<string>('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [analysisComplete, setAnalysisComplete] = useState(false);
  const { toast } = useToast();

  // Mock analysis data - in real app, this would come from your Python backend
  const mockAnalysisData = {
    overallScore: 78,
    atsCompatibility: 82,
    keywordMatch: 75,
    sectionCompleteness: 80,
    matchedKeywords: ['Python', 'React', 'AWS', 'Machine Learning', 'API Development', 'Git', 'Agile', 'Docker'],
    missingKeywords: ['Kubernetes', 'CI/CD', 'Microservices', 'GraphQL', 'Leadership', 'Team Management'],
    suggestions: [
      {
        category: 'Technical Skills',
        priority: 'High' as const,
        description: 'Add Kubernetes and CI/CD experience to match job requirements',
        impact: 'Could increase your match score by 12%'
      },
      {
        category: 'Leadership Experience',
        priority: 'Medium' as const,
        description: 'Highlight any team leadership or mentoring experience',
        impact: 'Improves cultural fit score for senior roles'
      },
      {
        category: 'Project Impact',
        priority: 'High' as const,
        description: 'Quantify achievements with specific metrics and business impact',
        impact: 'ATS systems favor measurable results'
      }
    ],
    companyFit: {
      score: 76,
      strengths: [
        'Strong technical background aligns with company culture',
        'Experience with company tech stack (AWS, Python)',
        'Education background matches job requirements'
      ],
      weaknesses: [
        'Limited leadership experience for senior role',
        'Missing some preferred certifications',
        'Could emphasize customer obsession more'
      ]
    },
    sectionAnalysis: [
      {
        section: 'Contact Information',
        score: 95,
        feedback: 'Complete and professional contact details',
        status: 'Good' as const
      },
      {
        section: 'Professional Summary',
        score: 70,
        feedback: 'Could be more specific to the target role and company',
        status: 'Needs Improvement' as const
      },
      {
        section: 'Technical Skills',
        score: 85,
        feedback: 'Good coverage of relevant technologies',
        status: 'Good' as const
      },
      {
        section: 'Work Experience',
        score: 75,
        feedback: 'Strong experience but needs more quantified achievements',
        status: 'Needs Improvement' as const
      },
      {
        section: 'Education',
        score: 90,
        feedback: 'Relevant degree and additional certifications',
        status: 'Good' as const
      },
      {
        section: 'Projects',
        score: 65,
        feedback: 'Include more detailed project descriptions',
        status: 'Needs Improvement' as const
      }
    ]
  };

  const steps: Step[] = [
    {
      id: 'upload',
      title: 'Upload Resume',
      description: 'Upload your resume in PDF or DOCX format',
      icon: <Upload className="w-5 h-5" />,
      completed: !!resumeFile
    },
    {
      id: 'company',
      title: 'Select Company',
      description: 'Choose your target company for ATS simulation',
      icon: <Target className="w-5 h-5" />,
      completed: !!selectedCompany
    },
    {
      id: 'job-description',
      title: 'Job Description',
      description: 'Provide the job description to analyze against',
      icon: <FileText className="w-5 h-5" />,
      completed: !!jobDescription
    },
    {
      id: 'analysis',
      title: 'Analysis',
      description: 'AI-powered resume analysis and scoring',
      icon: <Brain className="w-5 h-5" />,
      completed: analysisComplete
    }
  ];

  const handleStartAnalysis = async () => {
    if (!resumeFile || !selectedCompany || !jobDescription) {
      toast({
        title: "Missing Information",
        description: "Please complete all steps before starting analysis",
        variant: "destructive",
      });
      return;
    }

    setIsAnalyzing(true);
    setAnalysisProgress(0);
    setCurrentStep(3);

    // Simulate analysis progress
    const progressInterval = setInterval(() => {
      setAnalysisProgress((prev) => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          setIsAnalyzing(false);
          setAnalysisComplete(true);
          toast({
            title: "Analysis Complete",
            description: `Your resume has been analyzed for ${selectedCompany.name}`,
          });
          return 100;
        }
        return prev + 2;
      });
    }, 100);
  };

  const resetAnalysis = () => {
    setCurrentStep(0);
    setResumeFile(null);
    setSelectedCompany(null);
    setJobDescription('');
    setIsAnalyzing(false);
    setAnalysisProgress(0);
    setAnalysisComplete(false);
  };

  const downloadReport = () => {
    toast({
      title: "Report Downloaded",
      description: "Your detailed analysis report has been downloaded",
    });
  };

  if (analysisComplete) {
    return (
      <div className="max-w-6xl mx-auto p-6">
        <div className="mb-6">
          <Button 
            variant="ghost" 
            onClick={resetAnalysis}
            className="mb-4"
          >
            <ArrowLeft className="w-4 h-4" />
            Analyze Another Resume
          </Button>
        </div>
        
        <AnalysisResults
          analysisData={mockAnalysisData}
          companyName={selectedCompany?.name || ''}
          onReanalyze={resetAnalysis}
          onDownloadReport={downloadReport}
        />
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Progress Steps */}
      <Card className="p-6 mb-8">
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Resume Analysis Process</h2>
          
          <div className="grid md:grid-cols-4 gap-4">
            {steps.map((step, index) => (
              <div
                key={step.id}
                className={`
                  flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-all duration-200
                  ${currentStep === index 
                    ? 'bg-primary/10 border-2 border-primary/20' 
                    : step.completed 
                      ? 'bg-success/10 border border-success/20'
                      : 'bg-muted/50 border border-border'
                  }
                `}
                onClick={() => !isAnalyzing && setCurrentStep(index)}
              >
                <div className={`
                  w-8 h-8 rounded-full flex items-center justify-center
                  ${step.completed 
                    ? 'bg-success text-success-foreground' 
                    : currentStep === index
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted text-muted-foreground'
                  }
                `}>
                  {step.completed ? <CheckCircle className="w-4 h-4" /> : step.icon}
                </div>
                <div>
                  <p className="font-medium text-sm">{step.title}</p>
                  <p className="text-xs text-muted-foreground">{step.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </Card>

      {/* Analysis Progress */}
      {isAnalyzing && (
        <Card className="p-6 mb-8">
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <Brain className="w-6 h-6 text-primary animate-pulse" />
              <div>
                <h3 className="font-semibold">Analyzing Your Resume</h3>
                <p className="text-muted-foreground text-sm">
                  Running AI analysis for {selectedCompany?.name} ATS simulation...
                </p>
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Progress</span>
                <span>{analysisProgress}%</span>
              </div>
              <Progress value={analysisProgress} className="h-3" />
            </div>
            
            <div className="grid md:grid-cols-3 gap-4 text-sm">
              <div className={`flex items-center gap-2 ${analysisProgress > 30 ? 'text-success' : 'text-muted-foreground'}`}>
                <CheckCircle className="w-4 h-4" />
                Resume parsing complete
              </div>
              <div className={`flex items-center gap-2 ${analysisProgress > 60 ? 'text-success' : 'text-muted-foreground'}`}>
                <Clock className="w-4 h-4" />
                ATS simulation running
              </div>
              <div className={`flex items-center gap-2 ${analysisProgress > 90 ? 'text-success' : 'text-muted-foreground'}`}>
                <Brain className="w-4 h-4" />
                Generating insights
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* Step Content */}
      <div className="space-y-6">
        {currentStep === 0 && (
          <FileUpload
            onFileSelect={setResumeFile}
            acceptedTypes={['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']}
            maxSize={10 * 1024 * 1024} // 10MB
            label="Upload Your Resume"
            description="Upload your resume in PDF or DOCX format for analysis"
            selectedFile={resumeFile}
          />
        )}

        {currentStep === 1 && (
          <CompanySelector
            onCompanySelect={setSelectedCompany}
            selectedCompany={selectedCompany}
          />
        )}

        {currentStep === 2 && (
          <JobDescriptionUpload
            onJobDescriptionSubmit={setJobDescription}
            jobDescription={jobDescription}
          />
        )}

        {/* Navigation */}
        {!isAnalyzing && (
          <div className="flex justify-between">
            <Button
              variant="outline"
              onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
              disabled={currentStep === 0}
            >
              Previous
            </Button>

            <div className="flex gap-2">
              {currentStep < 3 && (
                <Button
                  onClick={() => setCurrentStep(Math.min(3, currentStep + 1))}
                  disabled={
                    (currentStep === 0 && !resumeFile) ||
                    (currentStep === 1 && !selectedCompany) ||
                    (currentStep === 2 && !jobDescription)
                  }
                >
                  Next
                </Button>
              )}

              {currentStep === 2 && resumeFile && selectedCompany && jobDescription && (
                <Button
                  variant="hero"
                  onClick={handleStartAnalysis}
                  className="ml-2"
                >
                  <Brain className="w-4 h-4" />
                  Start Analysis
                </Button>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};