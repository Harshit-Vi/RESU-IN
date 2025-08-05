import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  TrendingUp, 
  TrendingDown, 
  AlertTriangle, 
  CheckCircle, 
  Target, 
  Brain,
  FileText,
  Lightbulb,
  Download,
  RefreshCw
} from "lucide-react";

interface AnalysisData {
  overallScore: number;
  atsCompatibility: number;
  keywordMatch: number;
  sectionCompleteness: number;
  matchedKeywords: string[];
  missingKeywords: string[];
  suggestions: {
    category: string;
    priority: 'High' | 'Medium' | 'Low';
    description: string;
    impact: string;
  }[];
  companyFit: {
    score: number;
    strengths: string[];
    weaknesses: string[];
  };
  sectionAnalysis: {
    section: string;
    score: number;
    feedback: string;
    status: 'Good' | 'Needs Improvement' | 'Missing';
  }[];
}

interface AnalysisResultsProps {
  analysisData: AnalysisData;
  companyName: string;
  onReanalyze: () => void;
  onDownloadReport: () => void;
}

export const AnalysisResults = ({ 
  analysisData, 
  companyName, 
  onReanalyze, 
  onDownloadReport 
}: AnalysisResultsProps) => {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-success';
    if (score >= 60) return 'text-warning';
    return 'text-destructive';
  };

  const getScoreBg = (score: number) => {
    if (score >= 80) return 'bg-success/10';
    if (score >= 60) return 'bg-warning/10';
    return 'bg-destructive/10';
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'High': return 'bg-destructive/10 text-destructive border-destructive/20';
      case 'Medium': return 'bg-warning/10 text-warning border-warning/20';
      case 'Low': return 'bg-success/10 text-success border-success/20';
      default: return 'bg-muted text-muted-foreground';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'Good': return <CheckCircle className="w-4 h-4 text-success" />;
      case 'Needs Improvement': return <AlertTriangle className="w-4 h-4 text-warning" />;
      case 'Missing': return <TrendingDown className="w-4 h-4 text-destructive" />;
      default: return <CheckCircle className="w-4 h-4 text-muted-foreground" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="p-6 bg-gradient-secondary">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
              <Brain className="w-6 h-6 text-primary" />
            </div>
            <div>
              <h2 className="text-xl font-bold">Analysis Complete</h2>
              <p className="text-muted-foreground">ATS Simulation for {companyName}</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={onReanalyze} size="sm">
              <RefreshCw className="w-4 h-4" />
              Re-analyze
            </Button>
            <Button variant="professional" onClick={onDownloadReport} size="sm">
              <Download className="w-4 h-4" />
              Download Report
            </Button>
          </div>
        </div>

        {/* Overall Score */}
        <div className="grid md:grid-cols-4 gap-4">
          <Card className={`p-4 ${getScoreBg(analysisData.overallScore)}`}>
            <div className="text-center">
              <div className={`text-2xl font-bold ${getScoreColor(analysisData.overallScore)}`}>
                {analysisData.overallScore}%
              </div>
              <p className="text-sm text-muted-foreground">Overall Score</p>
            </div>
          </Card>
          
          <Card className={`p-4 ${getScoreBg(analysisData.atsCompatibility)}`}>
            <div className="text-center">
              <div className={`text-2xl font-bold ${getScoreColor(analysisData.atsCompatibility)}`}>
                {analysisData.atsCompatibility}%
              </div>
              <p className="text-sm text-muted-foreground">ATS Compatibility</p>
            </div>
          </Card>
          
          <Card className={`p-4 ${getScoreBg(analysisData.keywordMatch)}`}>
            <div className="text-center">
              <div className={`text-2xl font-bold ${getScoreColor(analysisData.keywordMatch)}`}>
                {analysisData.keywordMatch}%
              </div>
              <p className="text-sm text-muted-foreground">Keyword Match</p>
            </div>
          </Card>
          
          <Card className={`p-4 ${getScoreBg(analysisData.sectionCompleteness)}`}>
            <div className="text-center">
              <div className={`text-2xl font-bold ${getScoreColor(analysisData.sectionCompleteness)}`}>
                {analysisData.sectionCompleteness}%
              </div>
              <p className="text-sm text-muted-foreground">Section Complete</p>
            </div>
          </Card>
        </div>
      </Card>

      {/* Detailed Analysis */}
      <Tabs defaultValue="keywords" className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="keywords">Keywords</TabsTrigger>
          <TabsTrigger value="sections">Sections</TabsTrigger>
          <TabsTrigger value="suggestions">Suggestions</TabsTrigger>
          <TabsTrigger value="company-fit">Company Fit</TabsTrigger>
        </TabsList>

        <TabsContent value="keywords" className="space-y-4">
          <div className="grid md:grid-cols-2 gap-6">
            <Card className="p-6">
              <div className="flex items-center gap-2 mb-4">
                <CheckCircle className="w-5 h-5 text-success" />
                <h3 className="font-semibold">Matched Keywords</h3>
                <Badge className="bg-success/10 text-success">
                  {analysisData.matchedKeywords.length}
                </Badge>
              </div>
              <div className="flex flex-wrap gap-2">
                {analysisData.matchedKeywords.map((keyword, index) => (
                  <Badge key={index} className="bg-success/10 text-success border-success/20">
                    {keyword}
                  </Badge>
                ))}
              </div>
            </Card>

            <Card className="p-6">
              <div className="flex items-center gap-2 mb-4">
                <AlertTriangle className="w-5 h-5 text-warning" />
                <h3 className="font-semibold">Missing Keywords</h3>
                <Badge className="bg-warning/10 text-warning">
                  {analysisData.missingKeywords.length}
                </Badge>
              </div>
              <div className="flex flex-wrap gap-2">
                {analysisData.missingKeywords.map((keyword, index) => (
                  <Badge key={index} className="bg-warning/10 text-warning border-warning/20">
                    {keyword}
                  </Badge>
                ))}
              </div>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="sections" className="space-y-4">
          <div className="grid gap-4">
            {analysisData.sectionAnalysis.map((section, index) => (
              <Card key={index} className="p-6">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    {getStatusIcon(section.status)}
                    <h3 className="font-semibold">{section.section}</h3>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className={`text-lg font-bold ${getScoreColor(section.score)}`}>
                      {section.score}%
                    </div>
                    <Progress value={section.score} className="w-20" />
                  </div>
                </div>
                <p className="text-muted-foreground text-sm">{section.feedback}</p>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="suggestions" className="space-y-4">
          <div className="grid gap-4">
            {analysisData.suggestions.map((suggestion, index) => (
              <Card key={index} className="p-6">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <Lightbulb className="w-5 h-5 text-primary" />
                    <h3 className="font-semibold">{suggestion.category}</h3>
                  </div>
                  <Badge className={getPriorityColor(suggestion.priority)}>
                    {suggestion.priority} Priority
                  </Badge>
                </div>
                <p className="text-muted-foreground text-sm mb-2">{suggestion.description}</p>
                <div className="flex items-center gap-2 text-xs">
                  <Target className="w-3 h-3 text-primary" />
                  <span className="text-primary">Impact: {suggestion.impact}</span>
                </div>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="company-fit" className="space-y-4">
          <Card className="p-6">
            <div className="space-y-6">
              <div className="text-center">
                <div className={`text-4xl font-bold ${getScoreColor(analysisData.companyFit.score)} mb-2`}>
                  {analysisData.companyFit.score}%
                </div>
                <p className="text-muted-foreground">Company Fit Score</p>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-semibold text-success mb-3 flex items-center gap-2">
                    <TrendingUp className="w-4 h-4" />
                    Strengths
                  </h3>
                  <ul className="space-y-2">
                    {analysisData.companyFit.strengths.map((strength, index) => (
                      <li key={index} className="flex items-start gap-2 text-sm">
                        <CheckCircle className="w-4 h-4 text-success mt-0.5 flex-shrink-0" />
                        <span>{strength}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h3 className="font-semibold text-warning mb-3 flex items-center gap-2">
                    <TrendingDown className="w-4 h-4" />
                    Areas for Improvement
                  </h3>
                  <ul className="space-y-2">
                    {analysisData.companyFit.weaknesses.map((weakness, index) => (
                      <li key={index} className="flex items-start gap-2 text-sm">
                        <AlertTriangle className="w-4 h-4 text-warning mt-0.5 flex-shrink-0" />
                        <span>{weakness}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};