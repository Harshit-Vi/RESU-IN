import { useState } from 'react';
import { HeroSection } from '@/components/HeroSection';
import { ResumeAnalyzer } from '@/components/ResumeAnalyzer';

const Index = () => {
  const [showAnalyzer, setShowAnalyzer] = useState(false);

  if (showAnalyzer) {
    return (
      <div className="min-h-screen bg-background">
        <ResumeAnalyzer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <HeroSection onGetStarted={() => setShowAnalyzer(true)} />
    </div>
  );
};

export default Index;
