import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Brain, Target, Zap, TrendingUp } from "lucide-react";

interface HeroSectionProps {
  onGetStarted: () => void;
}

export const HeroSection = ({ onGetStarted }: HeroSectionProps) => {
  return (
    <div className="relative min-h-screen bg-gradient-hero flex flex-col justify-center items-center overflow-hidden">
      {/* Background Animation */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        {/* Main Hero Content */}
        <div className="space-y-8 mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 text-primary font-medium">
            <Brain className="w-4 h-4" />
            <span>AI-Powered Resume Intelligence</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent leading-tight">
            RESUIN
          </h1>
          
          <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Advanced Resume Analyzer & Company-Specific ATS Simulator
          </p>
          
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Decode how companies think. Get personalized insights with 80%+ ATS simulation accuracy 
            and transform your resume for your target companies.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              onClick={onGetStarted}
              variant="hero" 
              size="xl"
              className="group"
            >
              <Zap className="w-5 h-5 group-hover:rotate-12 transition-transform" />
              Analyze My Resume
            </Button>
            <Button 
              variant="professional" 
              size="xl"
            >
              <Target className="w-5 h-5" />
              View Demo
            </Button>
          </div>
        </div>

        {/* Feature Cards */}
        <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <Card className="p-6 bg-card/50 backdrop-blur-sm border-border/50 hover:shadow-elegant transition-all duration-300 hover:scale-[1.02]">
            <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 mx-auto">
              <Target className="w-6 h-6 text-primary" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Company-Specific ATS</h3>
            <p className="text-muted-foreground text-sm">
              Simulate real ATS logic for Amazon, TCS, and other major companies with 80%+ accuracy
            </p>
          </Card>

          <Card className="p-6 bg-card/50 backdrop-blur-sm border-border/50 hover:shadow-elegant transition-all duration-300 hover:scale-[1.02]">
            <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 mx-auto">
              <Brain className="w-6 h-6 text-primary" />
            </div>
            <h3 className="text-lg font-semibold mb-2">AI-Powered Analysis</h3>
            <p className="text-muted-foreground text-sm">
              Advanced NLP and machine learning algorithms analyze every aspect of your resume
            </p>
          </Card>

          <Card className="p-6 bg-card/50 backdrop-blur-sm border-border/50 hover:shadow-elegant transition-all duration-300 hover:scale-[1.02]">
            <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 mx-auto">
              <TrendingUp className="w-6 h-6 text-primary" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Actionable Insights</h3>
            <p className="text-muted-foreground text-sm">
              Get specific suggestions and improvements tailored to your target company
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
};