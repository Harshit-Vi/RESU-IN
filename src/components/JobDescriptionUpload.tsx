import { useState } from 'react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { FileText, Link, Type, Sparkles } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface JobDescriptionUploadProps {
  onJobDescriptionSubmit: (jd: string) => void;
  jobDescription?: string;
}

export const JobDescriptionUpload = ({ onJobDescriptionSubmit, jobDescription }: JobDescriptionUploadProps) => {
  const [jdText, setJdText] = useState(jobDescription || '');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async () => {
    if (jdText.trim().length < 100) {
      toast({
        title: "Job Description Too Short",
        description: "Please provide a more detailed job description (at least 100 characters).",
        variant: "destructive",
      });
      return;
    }

    setIsAnalyzing(true);
    
    // Simulate analysis delay
    setTimeout(() => {
      setIsAnalyzing(false);
      onJobDescriptionSubmit(jdText);
      toast({
        title: "Job Description Analyzed",
        description: "Successfully extracted key requirements and skills.",
      });
    }, 1500);
  };

  const sampleJobs = [
    {
      title: "Software Engineer",
      company: "Tech Company",
      preview: "We are looking for a skilled Software Engineer to join our team. Experience with React, Node.js, and AWS required..."
    },
    {
      title: "Data Scientist",
      company: "AI Startup",
      preview: "Seeking a Data Scientist with expertise in Python, Machine Learning, and statistical analysis. PhD preferred..."
    },
    {
      title: "Product Manager",
      company: "Fortune 500",
      preview: "Product Manager role focusing on strategic planning, cross-functional collaboration, and user experience..."
    }
  ];

  const getWordCount = () => jdText.trim().split(/\s+/).filter(word => word.length > 0).length;
  const wordCount = getWordCount();

  if (jobDescription) {
    return (
      <Card className="p-6 border-2 border-primary/20 bg-primary/5">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                <FileText className="w-5 h-5 text-primary" />
              </div>
              <div>
                <h3 className="font-medium">Job Description Loaded</h3>
                <p className="text-sm text-muted-foreground">{wordCount} words</p>
              </div>
            </div>
            <Badge className="bg-success/10 text-success border-success/20">
              Ready
            </Badge>
          </div>
          
          <div className="max-h-32 overflow-y-auto">
            <p className="text-sm text-muted-foreground">
              {jobDescription.substring(0, 200)}...
            </p>
          </div>
          
          <Button
            variant="outline"
            onClick={() => {
              setJdText(jobDescription);
              onJobDescriptionSubmit('');
            }}
            className="w-full"
          >
            Edit Job Description
          </Button>
        </div>
      </Card>
    );
  }

  return (
    <Card className="p-6">
      <div className="space-y-6">
        <div>
          <h3 className="font-semibold text-lg flex items-center gap-2">
            <Type className="w-5 h-5 text-primary" />
            Job Description
          </h3>
          <p className="text-muted-foreground text-sm mt-1">
            Paste the complete job description to analyze requirements
          </p>
        </div>

        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="job-description">Job Description Text</Label>
            <Textarea
              id="job-description"
              placeholder="Paste the complete job description here..."
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
              className="min-h-[200px] resize-y"
            />
            <div className="flex justify-between items-center text-xs text-muted-foreground">
              <span>{wordCount} words</span>
              <span className={wordCount >= 50 ? 'text-success' : 'text-warning'}>
                {wordCount >= 50 ? '✓ Good length' : 'Add more details'}
              </span>
            </div>
          </div>

          <Button
            onClick={handleSubmit}
            disabled={jdText.trim().length < 100 || isAnalyzing}
            className="w-full"
            variant="professional"
          >
            {isAnalyzing ? (
              <>
                <Sparkles className="w-4 h-4 animate-spin" />
                Analyzing Job Description...
              </>
            ) : (
              <>
                <FileText className="w-4 h-4" />
                Analyze Job Description
              </>
            )}
          </Button>
        </div>

        {/* Sample Jobs for Demo */}
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <div className="h-px bg-border flex-1" />
            <span className="text-xs text-muted-foreground px-2">Or try a sample</span>
            <div className="h-px bg-border flex-1" />
          </div>

          <div className="grid gap-3">
            {sampleJobs.map((job, index) => (
              <Card 
                key={index}
                className="p-4 cursor-pointer hover:shadow-elegant transition-all duration-200 hover:scale-[1.01] border-border/50"
                onClick={() => setJdText(job.preview + "\n\nRequirements:\n- Bachelor's degree in relevant field\n- 3+ years of experience\n- Strong communication skills\n- Team collaboration\n- Problem-solving abilities")}
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium text-sm">{job.title}</h4>
                    <Badge variant="secondary" className="text-xs">{job.company}</Badge>
                  </div>
                  <p className="text-xs text-muted-foreground line-clamp-2">
                    {job.preview}
                  </p>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
};