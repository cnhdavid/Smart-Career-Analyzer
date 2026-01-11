import os
import re
import json
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from openai import OpenAI


class Recommendation(BaseModel):
    skill: str = Field(description="The skill to learn")
    priority: str = Field(description="Priority level: High, Medium, or Low")
    resource: str = Field(description="Learning resource name")
    timeframe: str = Field(description="Estimated time to learn")
    learning_tip: str = Field(description="One-sentence learning tip for the skill", default="")


class ResumeAnalysis(BaseModel):
    skills: List[str] = Field(description="List of key competencies and skills found in the resume")
    experience_years: float = Field(description="Years of professional experience")
    current_field: str = Field(description="The professional field/industry the candidate currently works in")
    role_matches: Dict[str, float] = Field(description="Match percentage for each suggested role (3 roles)")
    skill_gaps: Dict[str, List[str]] = Field(description="Missing skills for each role")
    recommendations: List[Recommendation] = Field(description="Top 3 learning recommendations")
    trending_industries: List[str] = Field(description="List of 3-5 industries that match the candidate's skill set")
    summary: str = Field(description="2-sentence professional verdict of the profile")
    ats_feedback: List[str] = Field(description="List of 3-5 ATS optimization tips and warnings", default=[])


class AIAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            print("WARNING: OPENAI_API_KEY environment variable is not set. Running in mock mode.")
            self.mock_mode = True
        else:
            self.mock_mode = False
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"ERROR: Failed to initialize OpenAI client: {str(e)}")
                self.mock_mode = True
        
        # No fixed roles - AI will dynamically determine roles based on CV
    
    def analyze(self, resume_text: str, target_role: Optional[str] = None, job_description: Optional[str] = None) -> Dict:
        if self.mock_mode:
            print("[INFO] Running in MOCK MODE - no API key configured")
            return self._mock_analysis(resume_text, target_role, job_description)
        else:
            print("[INFO] Running in LIVE AI MODE - API key found")
            return self._ai_analysis(resume_text, target_role, job_description)
    
    def _mock_analysis(self, resume_text: str, target_role: Optional[str] = None, job_description: Optional[str] = None) -> Dict:
        detected_skills = self._extract_skills_universal(resume_text)
        experience_years = self._extract_experience_simple(resume_text)
        current_field = self._detect_field(resume_text, detected_skills)
        
        # Handle job description matching
        if job_description:
            # Extract requirements from job description
            jd_skills = self._extract_skills_from_job_description(job_description)
            jd_role = self._extract_role_from_job_description(job_description)
            
            # Primary role is from job description
            suggested_roles = [jd_role] + self._suggest_roles(current_field, jd_role)[:2]
            
            role_matches = {}
            skill_gaps = {}
            
            # Calculate match for the target job
            matched_skills = [s for s in detected_skills if s.lower() in [r.lower() for r in jd_skills]]
            match_percentage = (len(matched_skills) / max(len(jd_skills), 1)) * 100
            role_matches[jd_role] = round(min(match_percentage, 95), 1)
            
            missing_skills = [s for s in jd_skills if s.lower() not in [d.lower() for d in detected_skills]]
            skill_gaps[jd_role] = missing_skills[:5]
            
            # Calculate matches for other suggested roles
            for role in suggested_roles[1:]:
                required_skills = self._get_role_requirements(role, current_field)
                matched_skills = [s for s in detected_skills if s.lower() in [r.lower() for r in required_skills]]
                match_percentage = (len(matched_skills) / max(len(required_skills), 1)) * 100
                role_matches[role] = round(min(match_percentage, 95), 1)
                
                missing_skills = [s for s in required_skills if s.lower() not in [d.lower() for d in detected_skills]]
                skill_gaps[role] = missing_skills[:5]
        else:
            # Original logic for no job description
            if target_role:
                suggested_roles = [target_role] + self._suggest_roles(current_field, target_role)[:2]
            else:
                suggested_roles = self._suggest_roles(current_field)
            
            role_matches = {}
            skill_gaps = {}
            
            for role in suggested_roles:
                required_skills = self._get_role_requirements(role, current_field)
                matched_skills = [s for s in detected_skills if s.lower() in [r.lower() for r in required_skills]]
                match_percentage = (len(matched_skills) / max(len(required_skills), 1)) * 100
                role_matches[role] = round(min(match_percentage, 95), 1)
                
                missing_skills = [s for s in required_skills if s.lower() not in [d.lower() for d in detected_skills]]
                skill_gaps[role] = missing_skills[:5]
        
        # Dynamic categories based on field
        categories = self._get_field_categories(current_field)
        user_scores = self._calculate_universal_scores(detected_skills, categories)
        
        radar_data = {
            "labels": categories,
            "datasets": [
                {
                    "label": "Your Competencies",
                    "data": user_scores
                },
                {
                    "label": "Industry Standard",
                    "data": [80, 75, 70, 75, 65]
                }
            ]
        }
        
        # Trending industries
        trending_industries = self._identify_trending_industries(detected_skills, current_field)
        
        top_role = max(role_matches.items(), key=lambda x: x[1])[0]
        target_for_recs = target_role if target_role else top_role
        
        recommendations = []
        gaps_for_target = skill_gaps.get(target_for_recs, [])
        
        for i, skill in enumerate(gaps_for_target[:3]):
            priority = "High" if i == 0 else "Medium"
            recommendations.append({
                "skill": skill,
                "priority": priority,
                "resource": self._get_learning_resource(skill),
                "timeframe": self._get_timeframe(skill),
                "learning_tip": self._get_learning_tip(skill)
            })
        
        if len(recommendations) < 3:
            default_skills = self._get_default_skills_for_field(current_field)
            for skill in default_skills:
                if len(recommendations) >= 3:
                    break
                if skill not in detected_skills:
                    recommendations.append({
                        "skill": skill,
                        "priority": "Low",
                        "resource": self._get_learning_resource(skill),
                        "timeframe": self._get_timeframe(skill),
                        "learning_tip": self._get_learning_tip(skill)
                    })
        
        summary = self._generate_summary(detected_skills, experience_years, top_role, role_matches[top_role])
        
        # Generate ATS feedback
        ats_feedback = self._generate_ats_feedback(resume_text, detected_skills, job_description)
        
        return {
            "skills": detected_skills,
            "experience_years": experience_years,
            "current_field": current_field,
            "role_matches": role_matches,
            "skill_gaps": skill_gaps,
            "radar_data": radar_data,
            "recommendations": recommendations,
            "trending_industries": trending_industries,
            "summary": summary,
            "ats_feedback": ats_feedback
        }
    
    def _ai_analysis(self, resume_text: str, target_role: Optional[str] = None, job_description: Optional[str] = None) -> Dict:
        try:
            # Check API key first
            if not self.api_key:
                print("[AI ANALYSIS ERROR] No API key available")
                raise ValueError("OpenAI API key is not configured. Please set OPENAI_API_KEY environment variable.")
            
            # Handle job description vs target role
            if job_description:
                target_instruction = f"The user is applying for a SPECIFIC JOB. Act as a Technical Recruiter for this role. Job Description: {job_description[:1000]}. Calculate match score based ONLY on requirements in this job description. Extract the role title and required skills from the job description."
            elif target_role:
                target_instruction = f"The user wants to target the role: {target_role}. Include this as one of the 3 suggested roles."
            else:
                target_instruction = "Suggest the 3 most logical career next steps for this candidate."
            
            prompt = f"""
You are a Universal Career Consultant with expertise across ALL industries (Technology, Healthcare, Finance, Marketing, Sales, Operations, Education, Green Energy, Manufacturing, etc.).

Analyze the following resume and extract:
1. List of key competencies and skills (technical, soft skills, domain knowledge, certifications, tools, languages)
2. Years of professional experience (estimate if not explicit)
3. The candidate's current professional field/industry (e.g., "Software Development", "Healthcare Administration", "Digital Marketing", "Financial Services")
4. {target_instruction}
5. For each of the 3 suggested roles, calculate a match percentage (0-100) based on the candidate's skills and experience
6. For each role, identify 3-5 key skill gaps that would help the candidate transition or advance
7. Top 3 learning recommendations with priority (High/Medium/Low), resource name, timeframe, and a one-sentence learning tip
8. List 3-5 trending industries that currently match the candidate's skill set (e.g., "Healthcare Tech", "Renewable Energy", "FinTech", "E-commerce")
9. A 2-sentence professional summary/verdict of the candidate's profile
10. ATS Optimization Feedback: List 3-5 specific tips to improve ATS compatibility (check for: complex formatting, missing contact info, lack of standard section headings like "Experience" or "Skills", missing keywords, tables/graphics, unusual fonts, lack of quantifiable achievements)

Resume:
{resume_text[:3000]}

IMPORTANT: 
- Suggest roles across ANY industry, not just tech (e.g., Marketing Manager, Sales Director, Operations Lead, Healthcare Administrator, Financial Analyst)
- Be creative and consider lateral moves, promotions, and industry transitions
- Ensure the 3 roles are diverse and represent realistic career paths
- Match percentages should reflect genuine fit based on transferable skills

Return ONLY a valid JSON object with this exact structure:
{{
  "skills": ["skill1", "skill2", ...],
  "experience_years": 5.0,
  "current_field": "Field Name",
  "role_matches": {{"Role 1": 85.0, "Role 2": 75.0, "Role 3": 65.0}},
  "skill_gaps": {{"Role 1": ["skill1", "skill2"], "Role 2": [...], "Role 3": [...]}},
  "recommendations": [
    {{"skill": "Skill Name", "priority": "High", "resource": "Resource Name", "timeframe": "1-2 months", "learning_tip": "Tip here"}}
  ],
  "trending_industries": ["Industry 1", "Industry 2", ...],
  "summary": "Two sentence summary here.",
  "ats_feedback": ["Tip 1", "Tip 2", ...]
}}
"""
            
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a career analysis expert. Always respond with valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
                
                analysis = json.loads(response.choices[0].message.content)
                
                # Dynamic categories based on detected field
                current_field = analysis.get("current_field", "General")
                categories = self._get_field_categories(current_field)
                user_scores = self._calculate_universal_scores(analysis["skills"], categories)
                
                analysis["radar_data"] = {
                    "labels": categories,
                    "datasets": [
                        {
                            "label": "Your Competencies",
                            "data": user_scores
                        },
                        {
                            "label": "Industry Standard",
                            "data": [80, 75, 70, 75, 65]
                        }
                    ]
                }
                
                for rec in analysis.get("recommendations", []):
                    if "learning_tip" not in rec:
                        rec["learning_tip"] = self._get_learning_tip(rec.get("skill", ""))
                
                return analysis
            
            except json.JSONDecodeError as je:
                print(f"[AI ANALYSIS ERROR] JSON parsing failed: {str(je)}")
                print(f"[AI ANALYSIS ERROR] Response content: {response.choices[0].message.content if 'response' in locals() else 'No response'}")
                raise ValueError(f"Failed to parse AI response as JSON: {str(je)}")
            
            except Exception as api_error:
                print(f"[AI ANALYSIS ERROR] OpenAI API call failed: {type(api_error).__name__}")
                print(f"[AI ANALYSIS ERROR] Error message: {str(api_error)}")
                raise ValueError(f"OpenAI API error: {str(api_error)}")
        
        except Exception as e:
            import traceback
            error_details = {
                "error_type": type(e).__name__,
                "error_message": str(e),
                "traceback": traceback.format_exc()
            }
            print(f"[AI ANALYSIS ERROR] Type: {error_details['error_type']}")
            print(f"[AI ANALYSIS ERROR] Message: {error_details['error_message']}")
            print(f"[AI ANALYSIS ERROR] Full traceback:\n{error_details['traceback']}")
            print(f"[AI ANALYSIS] Falling back to mock mode")
            return self._mock_analysis(resume_text, target_role, job_description)
    
    def _extract_skills_universal(self, text: str) -> List[str]:
        # Universal skills across all industries
        universal_skills = [
            # Tech
            "Python", "JavaScript", "Java", "C++", "R", "SQL", "TypeScript",
            "React", "Angular", "Vue", "Node.js", "Django", "Flask", "FastAPI",
            "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
            "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy",
            "Docker", "Kubernetes", "AWS", "Azure", "GCP",
            "Git", "CI/CD", "REST API", "GraphQL", "MongoDB", "PostgreSQL",
            # Business & Management
            "Project Management", "Agile", "Scrum", "Leadership", "Team Management",
            "Strategic Planning", "Budget Management", "Stakeholder Management",
            "Change Management", "Risk Management", "Process Improvement",
            # Marketing & Sales
            "Digital Marketing", "SEO", "SEM", "Content Marketing", "Social Media Marketing",
            "Email Marketing", "Marketing Analytics", "CRM", "Salesforce", "HubSpot",
            "Sales Strategy", "Business Development", "Lead Generation", "Negotiation",
            # Finance & Accounting
            "Financial Analysis", "Financial Modeling", "Budgeting", "Forecasting",
            "Accounting", "Auditing", "Tax Planning", "Excel", "QuickBooks", "SAP",
            "Investment Analysis", "Portfolio Management", "Risk Assessment",
            # Healthcare
            "Patient Care", "Clinical Research", "Healthcare Administration",
            "Medical Coding", "HIPAA", "Electronic Health Records", "Nursing",
            # HR & Operations
            "Recruitment", "Talent Acquisition", "Employee Relations", "HR Policies",
            "Supply Chain Management", "Logistics", "Inventory Management",
            "Quality Assurance", "Lean Six Sigma", "Operations Management",
            # Soft Skills
            "Communication", "Problem Solving", "Critical Thinking", "Collaboration",
            "Time Management", "Adaptability", "Creativity", "Emotional Intelligence"
        ]
        
        detected = []
        text_lower = text.lower()
        
        for skill in universal_skills:
            if skill.lower() in text_lower:
                detected.append(skill)
        
        return detected[:20]
    
    def _extract_experience_simple(self, text: str) -> float:
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of)?\s*experience',
            r'experience[:\s]+(\d+)\+?\s*years?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return float(match.group(1))
        
        return 2.0
    
    def _detect_field(self, text: str, skills: List[str]) -> str:
        """Detect the professional field based on resume text and skills"""
        text_lower = text.lower()
        
        field_keywords = {
            "Software Development": ["software", "developer", "programming", "coding", "engineer"],
            "Data Science": ["data scientist", "machine learning", "analytics", "data analysis"],
            "Digital Marketing": ["marketing", "seo", "social media", "content marketing", "campaigns"],
            "Sales": ["sales", "business development", "account management", "revenue"],
            "Finance": ["financial", "accounting", "investment", "banking", "audit"],
            "Healthcare": ["healthcare", "medical", "patient", "clinical", "nursing", "hospital"],
            "Human Resources": ["hr", "recruitment", "talent acquisition", "employee relations"],
            "Operations": ["operations", "supply chain", "logistics", "process improvement"],
            "Project Management": ["project manager", "scrum master", "agile", "program management"],
            "Design": ["designer", "ux", "ui", "graphic design", "creative"],
            "Education": ["teacher", "instructor", "education", "training", "curriculum"]
        }
        
        field_scores = {}
        for field, keywords in field_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                field_scores[field] = score
        
        if field_scores:
            return max(field_scores.items(), key=lambda x: x[1])[0]
        return "General Business"
    
    def _suggest_roles(self, current_field: str, exclude_role: Optional[str] = None) -> List[str]:
        """Suggest 3 logical career next steps based on current field"""
        role_suggestions = {
            "Software Development": ["Senior Software Engineer", "Tech Lead", "Engineering Manager", "Solutions Architect", "DevOps Engineer"],
            "Data Science": ["Senior Data Scientist", "ML Engineer", "Data Engineering Manager", "AI Research Scientist", "Analytics Director"],
            "Digital Marketing": ["Marketing Manager", "Digital Marketing Director", "Growth Marketing Lead", "Brand Manager", "Content Strategy Director"],
            "Sales": ["Sales Manager", "Business Development Director", "Account Executive", "VP of Sales", "Revenue Operations Manager"],
            "Finance": ["Financial Analyst", "Finance Manager", "Investment Analyst", "Controller", "CFO"],
            "Healthcare": ["Healthcare Administrator", "Clinical Manager", "Medical Director", "Healthcare Consultant", "Patient Care Coordinator"],
            "Human Resources": ["HR Manager", "Talent Acquisition Lead", "People Operations Director", "HR Business Partner", "Chief People Officer"],
            "Operations": ["Operations Manager", "Supply Chain Director", "Process Improvement Manager", "COO", "Logistics Manager"],
            "Project Management": ["Senior Project Manager", "Program Manager", "Portfolio Manager", "PMO Director", "Agile Coach"],
            "Design": ["Senior Designer", "Design Manager", "Creative Director", "UX Director", "Product Designer"],
            "Education": ["Lead Instructor", "Curriculum Director", "Education Program Manager", "Dean", "Training Manager"],
            "General Business": ["Business Analyst", "Operations Manager", "Project Manager", "Strategy Consultant", "Product Manager"]
        }
        
        suggestions = role_suggestions.get(current_field, role_suggestions["General Business"])
        
        # Filter out the exclude_role if provided
        if exclude_role:
            suggestions = [r for r in suggestions if r.lower() != exclude_role.lower()]
        
        return suggestions[:3]
    
    def _get_role_requirements(self, role: str, field: str) -> List[str]:
        """Get required skills for a specific role"""
        # Generic requirements based on role type
        if "Manager" in role or "Director" in role or "Lead" in role:
            base_skills = ["Leadership", "Team Management", "Strategic Planning", "Communication", "Budget Management"]
        elif "Senior" in role:
            base_skills = ["Problem Solving", "Mentorship", "Technical Expertise", "Project Management"]
        elif "Engineer" in role or "Developer" in role:
            base_skills = ["Python", "Git", "Problem Solving", "Agile", "CI/CD"]
        elif "Analyst" in role:
            base_skills = ["Excel", "Data Analysis", "SQL", "Critical Thinking", "Communication"]
        elif "Designer" in role:
            base_skills = ["Creativity", "User Research", "Prototyping", "Collaboration", "Design Tools"]
        else:
            base_skills = ["Communication", "Problem Solving", "Collaboration", "Time Management"]
        
        # Add field-specific skills
        field_skills = {
            "Software Development": ["Python", "JavaScript", "Git", "Docker", "AWS"],
            "Data Science": ["Python", "Machine Learning", "SQL", "Statistics", "Data Visualization"],
            "Digital Marketing": ["SEO", "Google Analytics", "Content Marketing", "Social Media Marketing", "CRM"],
            "Sales": ["Salesforce", "Negotiation", "CRM", "Sales Strategy", "Lead Generation"],
            "Finance": ["Excel", "Financial Modeling", "Accounting", "Financial Analysis", "SAP"],
            "Healthcare": ["Patient Care", "Healthcare Administration", "HIPAA", "Electronic Health Records"],
            "Human Resources": ["Recruitment", "HR Policies", "Employee Relations", "Talent Management"],
            "Operations": ["Supply Chain Management", "Process Improvement", "Lean Six Sigma", "Logistics"],
            "Project Management": ["Agile", "Scrum", "Project Management", "Stakeholder Management"],
        }
        
        additional_skills = field_skills.get(field, ["Communication", "Leadership", "Problem Solving"])
        return list(set(base_skills + additional_skills))[:10]
    
    def _get_field_categories(self, field: str) -> List[str]:
        """Get radar chart categories based on professional field"""
        category_map = {
            "Software Development": ["Technical Skills", "Development Tools", "Architecture", "DevOps", "Collaboration"],
            "Data Science": ["Programming", "ML/AI", "Statistics", "Data Tools", "Visualization"],
            "Digital Marketing": ["Strategy", "Analytics", "Content", "Social Media", "Tools"],
            "Sales": ["Sales Skills", "CRM", "Communication", "Strategy", "Negotiation"],
            "Finance": ["Analysis", "Modeling", "Accounting", "Tools", "Compliance"],
            "Healthcare": ["Clinical Skills", "Administration", "Compliance", "Technology", "Patient Care"],
            "Human Resources": ["Recruitment", "Employee Relations", "Compliance", "Tools", "Strategy"],
            "Operations": ["Process Management", "Supply Chain", "Quality", "Tools", "Leadership"],
            "Project Management": ["Planning", "Execution", "Stakeholder Mgmt", "Tools", "Leadership"],
        }
        
        return category_map.get(field, ["Core Skills", "Tools", "Communication", "Leadership", "Strategy"])
    
    def _calculate_universal_scores(self, skills: List[str], categories: List[str]) -> List[float]:
        """Calculate scores for universal categories"""
        scores = []
        skills_lower = [s.lower() for s in skills]
        
        for category in categories:
            # Simple scoring: count related skills
            category_lower = category.lower()
            matched = sum(1 for skill in skills_lower if any(word in skill for word in category_lower.split()))
            score = min(100, matched * 15 + 40)
            scores.append(round(score, 1))
        
        return scores
    
    def _identify_trending_industries(self, skills: List[str], current_field: str) -> List[str]:
        """Identify trending industries that match the candidate's skills"""
        skills_lower = [s.lower() for s in skills]
        
        industry_keywords = {
            "HealthTech": ["healthcare", "medical", "patient", "clinical", "health"],
            "FinTech": ["finance", "banking", "investment", "payment", "blockchain"],
            "Green Energy": ["sustainability", "renewable", "energy", "environmental", "climate"],
            "E-commerce": ["ecommerce", "retail", "sales", "marketing", "logistics"],
            "AI & Machine Learning": ["machine learning", "ai", "deep learning", "nlp", "computer vision"],
            "Cybersecurity": ["security", "cybersecurity", "encryption", "compliance", "risk"],
            "Cloud Computing": ["aws", "azure", "gcp", "cloud", "devops"],
            "EdTech": ["education", "training", "learning", "curriculum", "teaching"],
            "SaaS": ["software", "saas", "api", "cloud", "subscription"],
            "Digital Marketing": ["marketing", "seo", "social media", "content", "analytics"]
        }
        
        industry_scores = {}
        for industry, keywords in industry_keywords.items():
            score = sum(1 for kw in keywords if any(kw in skill for skill in skills_lower))
            if score > 0:
                industry_scores[industry] = score
        
        # Sort by score and return top 3-5
        sorted_industries = sorted(industry_scores.items(), key=lambda x: x[1], reverse=True)
        return [industry for industry, _ in sorted_industries[:5]]
    
    def _get_default_skills_for_field(self, field: str) -> List[str]:
        """Get default recommended skills for a field"""
        default_skills = {
            "Software Development": ["Docker", "Kubernetes", "CI/CD", "TypeScript"],
            "Data Science": ["Deep Learning", "MLOps", "Big Data", "Cloud Platforms"],
            "Digital Marketing": ["Marketing Automation", "A/B Testing", "Google Ads", "Analytics"],
            "Sales": ["Sales Automation", "CRM Advanced", "Data Analysis", "Presentation Skills"],
            "Finance": ["Advanced Excel", "Power BI", "Financial Software", "Data Analysis"],
            "Healthcare": ["Healthcare IT", "Data Analytics", "Compliance Training", "EMR Systems"],
            "Human Resources": ["HR Analytics", "Applicant Tracking Systems", "Employee Engagement", "Compliance"],
            "Operations": ["Six Sigma", "ERP Systems", "Data Analytics", "Automation"],
            "Project Management": ["PMP Certification", "Advanced Agile", "Portfolio Management", "Risk Management"],
        }
        
        return default_skills.get(field, ["Leadership", "Communication", "Project Management"])
    
    def _calculate_category_scores(self, skills: List[str], categories: List[str]) -> List[float]:
        scores = []
        
        category_keywords = {
            "Programming": ["python", "javascript", "java", "c++", "typescript"],
            "ML/AI": ["machine learning", "deep learning", "tensorflow", "pytorch", "nlp"],
            "Frontend": ["react", "angular", "vue", "css", "html"],
            "Backend": ["node.js", "django", "flask", "fastapi", "sql"],
            "DevOps": ["docker", "kubernetes", "aws", "ci/cd", "git"]
        }
        
        for category in categories:
            keywords = category_keywords.get(category, [])
            matched = sum(1 for skill in skills if any(kw in skill.lower() for kw in keywords))
            score = min(100, (matched / max(len(keywords), 1)) * 100 + 20)
            scores.append(round(score, 1))
        
        return scores
    
    def _get_learning_resource(self, skill: str) -> str:
        resources = {
            "Python": "Python.org Official Tutorial",
            "JavaScript": "MDN Web Docs - JavaScript Guide",
            "React": "React Official Documentation",
            "Machine Learning": "Coursera - Machine Learning Specialization",
            "Deep Learning": "Deep Learning Specialization by Andrew Ng",
            "Docker": "Docker Official Documentation",
            "Kubernetes": "Kubernetes.io Interactive Tutorial",
            "AWS": "AWS Certified Solutions Architect Course",
            "SQL": "SQLBolt - Interactive SQL Tutorial",
            "TensorFlow": "TensorFlow Official Tutorials",
            "PyTorch": "PyTorch Tutorials",
            "Node.js": "Node.js Official Guides",
            "TypeScript": "TypeScript Handbook",
            "Statistics": "Khan Academy - Statistics & Probability",
            "Data Visualization": "D3.js in Action",
            "CI/CD": "GitHub Actions Documentation",
            "Git": "Pro Git Book (Free)"
        }
        return resources.get(skill, f"{skill} - Udemy/Coursera Course")
    
    def _get_timeframe(self, skill: str) -> str:
        timeframes = {
            "Python": "2-3 months",
            "JavaScript": "2-3 months",
            "React": "1-2 months",
            "Machine Learning": "3-4 months",
            "Deep Learning": "4-6 months",
            "Docker": "2-4 weeks",
            "Kubernetes": "1-2 months",
            "AWS": "2-3 months",
            "SQL": "1-2 months",
            "TensorFlow": "2-3 months",
            "PyTorch": "2-3 months",
            "Statistics": "2-3 months",
            "Git": "2-3 weeks"
        }
        return timeframes.get(skill, "1-3 months")
    
    def _get_learning_tip(self, skill: str) -> str:
        tips = {
            "Python": "Start with basic syntax and data structures, then build small projects to solidify your understanding.",
            "JavaScript": "Master the fundamentals before diving into frameworks - focus on ES6+ features and async programming.",
            "React": "Build component-based thinking by creating reusable UI components and understanding the virtual DOM.",
            "Machine Learning": "Begin with supervised learning algorithms and practice on real datasets from Kaggle.",
            "Deep Learning": "Start with neural network basics and implement models from scratch before using high-level frameworks.",
            "Docker": "Learn by containerizing your existing projects - start simple with single-container apps.",
            "Kubernetes": "Master Docker first, then deploy a simple app to understand pods, services, and deployments.",
            "AWS": "Get hands-on with the free tier - start with EC2, S3, and Lambda to understand core services.",
            "SQL": "Practice writing queries daily on platforms like LeetCode or HackerRank to build muscle memory.",
            "TensorFlow": "Follow official tutorials and implement classic models like CNNs and RNNs from scratch.",
            "PyTorch": "Start with tensor operations and autograd, then build neural networks using nn.Module.",
            "Node.js": "Build REST APIs and understand the event loop - async/await patterns are crucial.",
            "TypeScript": "Learn type annotations gradually by converting existing JavaScript projects to TypeScript.",
            "Statistics": "Focus on probability distributions and hypothesis testing - apply concepts to real-world data.",
            "Data Visualization": "Start with basic charts in libraries like Matplotlib or Chart.js before advanced visualizations.",
            "CI/CD": "Set up automated testing and deployment for a personal project using GitHub Actions or Jenkins.",
            "Git": "Practice branching strategies and learn to resolve merge conflicts through hands-on experience.",
            "Angular": "Understand TypeScript first, then master components, services, and dependency injection.",
            "Vue": "Start with the composition API and build reactive components with clear data flow.",
            "Django": "Learn the MVT pattern and build a full CRUD application with authentication.",
            "Flask": "Master routing and templates, then add database integration with SQLAlchemy.",
            "FastAPI": "Leverage type hints and automatic documentation - build async APIs for better performance.",
            "MongoDB": "Understand document-based data modeling and practice with aggregation pipelines.",
            "PostgreSQL": "Learn advanced features like JSON support, full-text search, and query optimization.",
            "GraphQL": "Start with schema design and resolvers - understand the difference from REST APIs.",
            "Redis": "Use it for caching and session storage in a real project to understand its speed benefits.",
            "Pandas": "Practice data manipulation with real datasets - master groupby, merge, and pivot operations.",
            "NumPy": "Focus on array operations and broadcasting - essential for data science and ML work.",
            "Scikit-learn": "Implement end-to-end ML pipelines including preprocessing, training, and evaluation.",
            "NLP": "Start with text preprocessing and basic techniques like TF-IDF before deep learning models.",
            "Computer Vision": "Learn image processing basics with OpenCV before diving into CNNs and object detection.",
            "Azure": "Explore Azure Portal and CLI - start with VMs, Storage, and Azure Functions.",
            "GCP": "Use the free tier to experiment with Compute Engine, Cloud Storage, and BigQuery."
        }
        return tips.get(skill, f"Practice {skill} through hands-on projects and online tutorials to build real-world experience.")
    
    def _generate_summary(self, skills: List[str], experience_years: float, top_role: str, match_score: float) -> str:
        skill_count = len(skills)
        
        if match_score >= 75:
            strength = "excellent"
            outlook = "well-positioned for senior roles"
        elif match_score >= 60:
            strength = "strong"
            outlook = "ready for mid-level positions with some upskilling"
        elif match_score >= 40:
            strength = "solid"
            outlook = "has a clear growth path with focused learning"
        else:
            strength = "developing"
            outlook = "should focus on building core competencies"
        
        summary = f"This candidate demonstrates a {strength} technical foundation with {skill_count} identified skills and {experience_years} years of experience, showing the best fit for {top_role} roles. "
        summary += f"They are {outlook} in their target domain."
        
        return summary
    
    def _extract_skills_from_job_description(self, job_description: str) -> List[str]:
        """Extract required skills from job description"""
        jd_lower = job_description.lower()
        detected_skills = []
        
        # Use the same universal skills list
        universal_skills = [
            "Python", "JavaScript", "Java", "C++", "R", "SQL", "TypeScript",
            "React", "Angular", "Vue", "Node.js", "Django", "Flask", "FastAPI",
            "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
            "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy",
            "Docker", "Kubernetes", "AWS", "Azure", "GCP",
            "Git", "CI/CD", "REST API", "GraphQL", "MongoDB", "PostgreSQL",
            "Project Management", "Agile", "Scrum", "Leadership", "Team Management",
            "Strategic Planning", "Budget Management", "Stakeholder Management",
            "Digital Marketing", "SEO", "SEM", "Content Marketing", "Social Media Marketing",
            "Salesforce", "HubSpot", "CRM", "Sales Strategy", "Business Development",
            "Financial Analysis", "Financial Modeling", "Budgeting", "Excel",
            "Communication", "Problem Solving", "Critical Thinking", "Collaboration"
        ]
        
        for skill in universal_skills:
            if skill.lower() in jd_lower:
                detected_skills.append(skill)
        
        return detected_skills[:15]
    
    def _extract_role_from_job_description(self, job_description: str) -> str:
        """Extract role title from job description"""
        lines = job_description.split('\n')
        first_line = lines[0].strip() if lines else "Target Role"
        
        # Common role patterns
        role_keywords = ["engineer", "manager", "director", "analyst", "developer", 
                        "designer", "specialist", "consultant", "coordinator", "lead"]
        
        for line in lines[:5]:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in role_keywords):
                return line.strip()[:50]
        
        return first_line[:50] if first_line else "Target Role"
    
    def _generate_ats_feedback(self, resume_text: str, skills: List[str], job_description: Optional[str] = None) -> List[str]:
        """Generate ATS optimization feedback"""
        feedback = []
        text_lower = resume_text.lower()
        
        # Check for contact information
        has_email = '@' in resume_text
        has_phone = any(char.isdigit() for char in resume_text[:200])
        
        if not has_email:
            feedback.append("⚠️ Missing email address - Add a professional email in the contact section")
        if not has_phone:
            feedback.append("⚠️ Missing phone number - Include your contact number for recruiters")
        
        # Check for standard section headings
        standard_sections = ["experience", "education", "skills", "work history"]
        missing_sections = [s for s in standard_sections if s not in text_lower]
        
        if len(missing_sections) >= 2:
            feedback.append(f"📋 Use standard section headings like 'Experience', 'Education', 'Skills' for better ATS parsing")
        
        # Check for quantifiable achievements
        has_numbers = bool(re.search(r'\d+%|\d+\+|increased|decreased|improved|reduced', text_lower))
        if not has_numbers:
            feedback.append("📊 Add quantifiable achievements (e.g., 'Increased sales by 25%', 'Managed team of 10')")
        
        # Check for keywords if job description provided
        if job_description:
            jd_skills = self._extract_skills_from_job_description(job_description)
            missing_keywords = [s for s in jd_skills if s.lower() not in text_lower]
            
            if len(missing_keywords) > 3:
                feedback.append(f"🎯 Missing key job requirements: {', '.join(missing_keywords[:3])} - Consider adding these if you have experience")
        
        # General ATS tips
        if len(feedback) < 3:
            feedback.append("✅ Use simple, clean formatting - Avoid tables, text boxes, headers/footers")
            feedback.append("✅ Save as .docx or PDF format - Ensure text is selectable, not images")
        
        if len(feedback) < 5:
            feedback.append("💡 Include relevant keywords from the job description naturally throughout your resume")
        
        return feedback[:5]
