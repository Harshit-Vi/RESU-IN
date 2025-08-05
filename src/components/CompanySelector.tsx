import { useState } from 'react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Building2, Target, Briefcase, Search } from "lucide-react";

interface Company {
  id: string;
  name: string;
  logo?: string;
  atsType: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  industry: string;
  description: string;
}

interface CompanySelectorProps {
  onCompanySelect: (company: Company) => void;
  selectedCompany?: Company | null;
}

const popularCompanies: Company[] = [
  {
    id: 'amazon',
    name: 'Amazon',
    atsType: 'Greenhouse + Custom',
    difficulty: 'Hard',
    industry: 'Technology',
    description: 'Focus on leadership principles, customer obsession, and scalability'
  },
  {
    id: 'google',
    name: 'Google',
    atsType: 'Google Hire',
    difficulty: 'Hard',
    industry: 'Technology',
    description: 'Emphasizes innovation, technical skills, and problem-solving'
  },
  {
    id: 'microsoft',
    name: 'Microsoft',
    atsType: 'SmartRecruiters',
    difficulty: 'Hard',
    industry: 'Technology',
    description: 'Values collaboration, growth mindset, and technical excellence'
  },
  {
    id: 'tcs',
    name: 'Tata Consultancy Services',
    atsType: 'TCS Custom ATS',
    difficulty: 'Medium',
    industry: 'IT Services',
    description: 'Focuses on certifications, domain expertise, and client delivery'
  },
  {
    id: 'infosys',
    name: 'Infosys',
    atsType: 'Workday',
    difficulty: 'Medium',
    industry: 'IT Services',
    description: 'Emphasizes continuous learning, agility, and digital transformation'
  },
  {
    id: 'wipro',
    name: 'Wipro',
    atsType: 'SuccessFactors',
    difficulty: 'Medium',
    industry: 'IT Services',
    description: 'Values innovation, sustainability, and diverse perspectives'
  }
];

export const CompanySelector = ({ onCompanySelect, selectedCompany }: CompanySelectorProps) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedIndustry, setSelectedIndustry] = useState<string>('all');

  const industries = ['all', ...Array.from(new Set(popularCompanies.map(c => c.industry)))];
  
  const filteredCompanies = popularCompanies.filter(company => {
    const matchesSearch = company.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesIndustry = selectedIndustry === 'all' || company.industry === selectedIndustry;
    return matchesSearch && matchesIndustry;
  });

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Easy': return 'bg-success/10 text-success border-success/20';
      case 'Medium': return 'bg-warning/10 text-warning border-warning/20';
      case 'Hard': return 'bg-destructive/10 text-destructive border-destructive/20';
      default: return 'bg-muted text-muted-foreground';
    }
  };

  if (selectedCompany) {
    return (
      <Card className="p-6 border-2 border-primary/20 bg-primary/5">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <Building2 className="w-6 h-6 text-primary" />
              </div>
              <div>
                <h3 className="font-semibold text-lg">{selectedCompany.name}</h3>
                <p className="text-sm text-muted-foreground">{selectedCompany.atsType}</p>
              </div>
            </div>
            <Badge className={getDifficultyColor(selectedCompany.difficulty)}>
              {selectedCompany.difficulty}
            </Badge>
          </div>
          
          <p className="text-sm text-muted-foreground">{selectedCompany.description}</p>
          
          <Button
            variant="outline"
            onClick={() => onCompanySelect(null as any)}
            className="w-full"
          >
            Change Company
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
            <Target className="w-5 h-5 text-primary" />
            Select Target Company
          </h3>
          <p className="text-muted-foreground text-sm mt-1">
            Choose the company you're applying to for ATS simulation
          </p>
        </div>

        {/* Search and Filter */}
        <div className="space-y-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
            <Input
              placeholder="Search companies..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
          
          <div className="space-y-2">
            <Label>Industry</Label>
            <Select value={selectedIndustry} onValueChange={setSelectedIndustry}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {industries.map(industry => (
                  <SelectItem key={industry} value={industry}>
                    {industry === 'all' ? 'All Industries' : industry}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Company Grid */}
        <div className="grid gap-4">
          {filteredCompanies.map((company) => (
            <Card 
              key={company.id}
              className="p-4 cursor-pointer hover:shadow-elegant transition-all duration-200 hover:scale-[1.01] border-border/50"
              onClick={() => onCompanySelect(company)}
            >
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                    <Building2 className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <h4 className="font-medium">{company.name}</h4>
                    <p className="text-xs text-muted-foreground">{company.atsType}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary" className="text-xs">
                    {company.industry}
                  </Badge>
                  <Badge className={getDifficultyColor(company.difficulty)}>
                    {company.difficulty}
                  </Badge>
                </div>
              </div>
              
              <p className="text-sm text-muted-foreground">{company.description}</p>
            </Card>
          ))}
        </div>

        {filteredCompanies.length === 0 && (
          <div className="text-center py-8">
            <Briefcase className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground">No companies found</p>
            <p className="text-sm text-muted-foreground">Try adjusting your search or filter</p>
          </div>
        )}
      </div>
    </Card>
  );
};