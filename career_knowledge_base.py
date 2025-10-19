"""
Career Knowledge Base for RAG Pipeline
Contains structured career information for retrieval
"""

CAREER_KNOWLEDGE_BASE = {
    "job_search": [
        {
            "id": "js_001",
            "content": "When searching for jobs, focus on keywords that match your skills and experience. Use specific job titles and include location preferences. Tailor your resume for each application by highlighting relevant skills mentioned in the job description.",
            "keywords": ["job search", "keywords", "resume", "application", "skills"],
            "category": "job_search"
        },
        {
            "id": "js_002", 
            "content": "Networking is crucial for job search success. Attend industry events, connect with professionals on LinkedIn, and reach out to alumni from your school. Many jobs are filled through referrals before being posted publicly.",
            "keywords": ["networking", "linkedin", "referrals", "connections", "industry events"],
            "category": "job_search"
        },
        {
            "id": "js_003",
            "content": "Create a strong online presence with a professional LinkedIn profile, portfolio website, and GitHub profile (for tech roles). Employers often research candidates online before interviews.",
            "keywords": ["online presence", "linkedin", "portfolio", "github", "professional profile"],
            "category": "job_search"
        }
    ],
    
    "interview_preparation": [
        {
            "id": "ip_001",
            "content": "Prepare for interviews by researching the company, understanding their mission and values, and preparing specific examples using the STAR method (Situation, Task, Action, Result) for behavioral questions.",
            "keywords": ["interview prep", "company research", "STAR method", "behavioral questions", "mission"],
            "category": "interview_preparation"
        },
        {
            "id": "ip_002",
            "content": "Practice common interview questions like 'Tell me about yourself', 'Why do you want to work here?', and 'What are your strengths and weaknesses?' Prepare concise, relevant answers that highlight your qualifications.",
            "keywords": ["common questions", "tell me about yourself", "strengths", "weaknesses", "practice"],
            "category": "interview_preparation"
        },
        {
            "id": "ip_003",
            "content": "For technical interviews, practice coding problems, system design questions, and be ready to explain your thought process. Use platforms like LeetCode, HackerRank, or CodeSignal for practice.",
            "keywords": ["technical interview", "coding", "system design", "leetcode", "hackerrank"],
            "category": "interview_preparation"
        }
    ],
    
    "resume_writing": [
        {
            "id": "rw_001",
            "content": "A strong resume should be 1-2 pages, use action verbs, include quantifiable achievements, and be tailored to each job. Use ATS-friendly formatting with standard fonts and clear section headers.",
            "keywords": ["resume", "action verbs", "achievements", "ATS", "formatting", "pages"],
            "category": "resume_writing"
        },
        {
            "id": "rw_002",
            "content": "Include relevant keywords from job descriptions in your resume. Use specific metrics and numbers to quantify your achievements. For example, 'Increased sales by 25%' is better than 'Improved sales performance'.",
            "keywords": ["keywords", "metrics", "quantify", "achievements", "job description"],
            "category": "resume_writing"
        },
        {
            "id": "rw_003",
            "content": "Your resume should include: Contact information, Professional summary, Work experience, Education, Skills, and relevant certifications. Optional sections include projects, volunteer work, or publications.",
            "keywords": ["contact info", "summary", "experience", "education", "skills", "certifications"],
            "category": "resume_writing"
        }
    ],
    
    "career_development": [
        {
            "id": "cd_001",
            "content": "Continuous learning is essential for career growth. Take online courses, attend workshops, earn certifications, and stay updated with industry trends. Consider both technical and soft skills development.",
            "keywords": ["learning", "courses", "certifications", "skills", "growth", "industry trends"],
            "category": "career_development"
        },
        {
            "id": "cd_002",
            "content": "Build a strong professional network by attending conferences, joining industry groups, participating in online communities, and maintaining relationships with colleagues and mentors.",
            "keywords": ["networking", "conferences", "industry groups", "mentors", "relationships"],
            "category": "career_development"
        },
        {
            "id": "cd_003",
            "content": "Set clear career goals and create a development plan. Identify skills gaps, seek feedback from managers, and take on challenging projects that help you grow professionally.",
            "keywords": ["career goals", "development plan", "skills gaps", "feedback", "challenging projects"],
            "category": "career_development"
        }
    ],
    
    "salary_negotiation": [
        {
            "id": "sn_001",
            "content": "Research salary ranges for your role and location using sites like Glassdoor, PayScale, or LinkedIn Salary Insights. Consider total compensation including benefits, bonuses, and equity.",
            "keywords": ["salary research", "glassdoor", "payscale", "compensation", "benefits", "bonuses"],
            "category": "salary_negotiation"
        },
        {
            "id": "sn_002",
            "content": "During salary negotiations, focus on your value and contributions. Be prepared to discuss your achievements and how you can help the company succeed. Practice your negotiation pitch beforehand.",
            "keywords": ["negotiation", "value", "contributions", "achievements", "pitch"],
            "category": "salary_negotiation"
        }
    ],
    
    "industry_insights": [
        {
            "id": "ii_001",
            "content": "Technology industry is rapidly evolving with trends in AI, cloud computing, cybersecurity, and remote work. Stay updated with latest technologies and consider specializing in high-demand areas.",
            "keywords": ["technology", "AI", "cloud computing", "cybersecurity", "remote work", "trends"],
            "category": "industry_insights"
        },
        {
            "id": "ii_002",
            "content": "Remote work has become more common, requiring strong communication skills, self-discipline, and proficiency with digital collaboration tools. Consider how to demonstrate these skills in applications.",
            "keywords": ["remote work", "communication", "collaboration tools", "self-discipline", "digital skills"],
            "category": "industry_insights"
        }
    ]
}

def get_knowledge_by_category(category):
    """Get all knowledge entries for a specific category"""
    return CAREER_KNOWLEDGE_BASE.get(category, [])

def search_knowledge(query, category=None):
    """Search knowledge base for relevant content"""
    query_lower = query.lower()
    results = []
    
    for cat, entries in CAREER_KNOWLEDGE_BASE.items():
        if category and cat != category:
            continue
            
        for entry in entries:
            # Check if query matches keywords or content
            if (any(keyword in query_lower for keyword in entry["keywords"]) or
                any(word in entry["content"].lower() for word in query_lower.split())):
                results.append(entry)
    
    return results

def get_all_knowledge():
    """Get all knowledge entries"""
    all_entries = []
    for entries in CAREER_KNOWLEDGE_BASE.values():
        all_entries.extend(entries)
    return all_entries
