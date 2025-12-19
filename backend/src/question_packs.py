"""
Question Packs Module
Provides job-specific and company-specific interview questions
"""

# Job Role-Specific Question Banks
JOB_ROLE_QUESTIONS = {
    "ML Engineer": {
        "technical": [
            "Explain the difference between supervised and unsupervised learning with examples.",
            "How would you handle imbalanced datasets in a classification problem?",
            "Walk me through the process of training a neural network from scratch.",
            "What's the difference between L1 and L2 regularization?",
            "How do you evaluate the performance of a machine learning model?",
            "Explain gradient descent and its variants.",
            "What is overfitting and how do you prevent it?",
            "Describe a machine learning project you've worked on.",
        ],
        "behavioral": [
            "Tell me about a time when your ML model didn't perform as expected.",
            "How do you stay updated with the latest ML research?",
            "Describe a situation where you had to explain a complex ML concept to non-technical stakeholders.",
        ],
        "system_design": [
            "How would you design a recommendation system for an e-commerce platform?",
            "Design a real-time fraud detection system.",
        ]
    },
    
    "Python Developer": {
        "technical": [
            "Explain the difference between lists and tuples in Python.",
            "What are decorators in Python and when would you use them?",
            "How does Python's garbage collection work?",
            "Explain the difference between @staticmethod and @classmethod.",
            "What are generators and why are they useful?",
            "How do you handle exceptions in Python?",
            "Explain the GIL (Global Interpreter Lock) in Python.",
            "What's the difference between deep copy and shallow copy?",
        ],
        "behavioral": [
            "Tell me about a challenging Python project you've worked on.",
            "How do you debug Python code?",
            "Describe your experience with Python frameworks like Django or Flask.",
        ],
        "coding": [
            "Write a function to reverse a string without using built-in methods.",
            "Implement a function to find the most frequent element in a list.",
        ]
    },
    
    "Data Analyst": {
        "technical": [
            "What's the difference between SQL and NoSQL databases?",
            "Explain the concept of data normalization.",
            "How do you handle missing data in a dataset?",
            "What visualization tools have you used and why?",
            "Explain the difference between INNER JOIN and LEFT JOIN.",
            "How do you identify outliers in data?",
            "What statistical methods do you use for data analysis?",
        ],
        "behavioral": [
            "Tell me about a time when you found insights from data that led to business decisions.",
            "How do you communicate complex data findings to non-technical stakeholders?",
            "Describe a situation where your analysis was challenged.",
        ],
        "case_study": [
            "Given sales data, how would you identify trends and make recommendations?",
            "How would you analyze customer churn for a subscription service?",
        ]
    },
    
    "Robotics Engineer": {
        "technical": [
            "Explain the difference between forward and inverse kinematics.",
            "How do you implement path planning for a mobile robot?",
            "What sensors would you use for autonomous navigation?",
            "Explain PID control and its applications in robotics.",
            "How do you handle sensor fusion in robotics?",
            "What's the difference between ROS and ROS2?",
        ],
        "behavioral": [
            "Tell me about a robotics project you've built from scratch.",
            "How do you debug hardware-software integration issues?",
        ],
        "system_design": [
            "Design a warehouse automation system using robots.",
        ]
    },
    
    "Cloud Engineer": {
        "technical": [
            "Explain the difference between IaaS, PaaS, and SaaS.",
            "How do you ensure high availability in cloud architecture?",
            "What's the difference between horizontal and vertical scaling?",
            "Explain containerization and its benefits.",
            "How do you implement CI/CD pipelines?",
            "What security measures do you implement in cloud deployments?",
            "Explain the concept of Infrastructure as Code.",
        ],
        "behavioral": [
            "Tell me about a time when you optimized cloud costs.",
            "How do you handle cloud service outages?",
        ],
        "system_design": [
            "Design a scalable web application architecture on AWS/Azure/GCP.",
        ]
    },
    
    "QA Engineer": {
        "technical": [
            "What's the difference between manual and automated testing?",
            "Explain the testing pyramid.",
            "How do you write effective test cases?",
            "What testing frameworks have you used?",
            "Explain regression testing and when it's needed.",
            "How do you perform API testing?",
            "What's the difference between smoke testing and sanity testing?",
        ],
        "behavioral": [
            "Tell me about a critical bug you found and how you reported it.",
            "How do you prioritize testing when time is limited?",
        ],
        "scenario": [
            "How would you test a login page?",
            "Design a test strategy for a mobile app.",
        ]
    }
}

# Company-Specific Interview Styles
COMPANY_STYLES = {
    "Google": {
        "focus": "Problem-solving, algorithms, system design, and Googleyness",
        "tone": "Collaborative, intellectually curious, focus on thought process",
        "difficulty": "High",
        "question_style": "Open-ended, focus on scalability and optimization",
        "principles": [
            "Think big and innovate",
            "Focus on user impact",
            "Collaborate effectively",
            "Be comfortable with ambiguity"
        ],
        "sample_questions": [
            "How would you design Google Maps?",
            "Estimate the number of tennis balls that fit in a school bus.",
            "Tell me about a time you solved a complex technical problem.",
        ]
    },
    
    "Amazon": {
        "focus": "Leadership principles, customer obsession, ownership",
        "tone": "Results-oriented, data-driven, high ownership",
        "difficulty": "High",
        "question_style": "STAR format behavioral + technical depth",
        "principles": [
            "Customer Obsession",
            "Ownership",
            "Invent and Simplify",
            "Bias for Action",
            "Deliver Results"
        ],
        "sample_questions": [
            "Tell me about a time you went above and beyond for a customer.",
            "Describe a situation where you had to make a decision with incomplete information.",
            "Give an example of when you took ownership of a difficult problem.",
        ]
    },
    
    "TCS": {
        "focus": "Process knowledge, teamwork, adaptability, domain knowledge",
        "tone": "Professional, process-oriented, team-focused",
        "difficulty": "Medium",
        "question_style": "Structured, focus on experience and learning ability",
        "principles": [
            "Client focus",
            "Team collaboration",
            "Continuous learning",
            "Process adherence"
        ],
        "sample_questions": [
            "How do you handle tight deadlines in a team environment?",
            "Tell me about your experience with Agile methodologies.",
            "How do you ensure quality in your deliverables?",
        ]
    },
    
    "Infosys": {
        "focus": "Technical skills, learning agility, cultural fit",
        "tone": "Formal, structured, emphasis on training and growth",
        "difficulty": "Medium",
        "question_style": "Mix of technical and behavioral, focus on potential",
        "principles": [
            "Learn and evolve",
            "Collaborate and innovate",
            "Client value creation",
            "Integrity and transparency"
        ],
        "sample_questions": [
            "How do you approach learning new technologies?",
            "Describe a project where you worked in a team.",
            "What interests you about working at Infosys?",
        ]
    },
    
    "Deloitte": {
        "focus": "Consulting skills, business acumen, communication",
        "tone": "Professional, client-focused, analytical",
        "difficulty": "Medium-High",
        "question_style": "Case studies, behavioral, business scenarios",
        "principles": [
            "Lead the way",
            "Serve with integrity",
            "Take care of each other",
            "Foster inclusion"
        ],
        "sample_questions": [
            "How would you advise a client looking to reduce costs?",
            "Tell me about a time you had to present complex information to stakeholders.",
            "Describe your approach to problem-solving in consulting.",
        ]
    },
    
    "Wipro": {
        "focus": "Technical competency, teamwork, adaptability",
        "tone": "Balanced, practical, growth-oriented",
        "difficulty": "Medium",
        "question_style": "Technical + behavioral, focus on real-world scenarios",
        "principles": [
            "Spirit of Wipro",
            "Unyielding integrity",
            "Respect for the individual",
            "Passion for excellence"
        ],
        "sample_questions": [
            "How do you handle conflicts in a team?",
            "Describe a technical challenge you overcame.",
            "What motivates you in your career?",
        ]
    },
    
    "Microsoft": {
        "focus": "Technical depth, growth mindset, collaboration",
        "tone": "Inclusive, innovative, focus on learning",
        "difficulty": "High",
        "question_style": "Technical problem-solving + behavioral, focus on impact",
        "principles": [
            "Growth mindset",
            "Customer obsession",
            "Diversity and inclusion",
            "One Microsoft"
        ],
        "sample_questions": [
            "How would you design a feature for Microsoft Teams?",
            "Tell me about a time you learned from failure.",
            "Describe how you've helped others grow.",
        ]
    }
}


def get_questions_for_role(role, count=5):
    """
    Get random questions for a specific job role
    
    Args:
        role: Job role (e.g., "ML Engineer")
        count: Number of questions to return
        
    Returns:
        List of questions
    """
    import random
    
    if role not in JOB_ROLE_QUESTIONS:
        return []
    
    role_data = JOB_ROLE_QUESTIONS[role]
    all_questions = []
    
    for category in role_data.values():
        all_questions.extend(category)
    
    return random.sample(all_questions, min(count, len(all_questions)))


def get_company_style_prompt(company):
    """
    Get interview style prompt for a specific company
    
    Args:
        company: Company name (e.g., "Google")
        
    Returns:
        Formatted prompt string
    """
    if company not in COMPANY_STYLES:
        return ""
    
    style = COMPANY_STYLES[company]
    
    prompt = f"""
You are conducting a {company} interview. Follow these guidelines:

**Interview Style:**
- Focus: {style['focus']}
- Tone: {style['tone']}
- Difficulty: {style['difficulty']}
- Question Style: {style['question_style']}

**Company Principles:**
{chr(10).join(f"- {p}" for p in style['principles'])}

**Example Questions:**
{chr(10).join(f"- {q}" for q in style['sample_questions'])}

Maintain {company}'s interview culture throughout the conversation.
"""
    
    return prompt


def generate_role_company_questions(role, company, count=3):
    """
    Generate questions combining role and company style
    
    Args:
        role: Job role
        company: Company name
        count: Number of questions
        
    Returns:
        List of tailored questions
    """
    import random
    
    role_questions = get_questions_for_role(role, count * 2)
    
    if company in COMPANY_STYLES:
        company_questions = COMPANY_STYLES[company]['sample_questions']
        # Mix role-specific and company-specific
        combined = role_questions + company_questions
        return random.sample(combined, min(count, len(combined)))
    
    return role_questions[:count]
