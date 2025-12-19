from typing import List, Optional, Dict
from dataclasses import dataclass, field

@dataclass
class Location:
    city: str = ""
    country_code: str = ""
    region: str = ""

@dataclass
class Profile:
    network: str = ""
    username: str = ""
    url: str = ""

@dataclass
class Basics:
    name: str = ""
    label: str = "" # Job Title
    image: str = ""
    email: str = ""
    phone: str = ""
    url: str = ""
    summary: str = ""
    location: Location = field(default_factory=Location)
    profiles: List[Profile] = field(default_factory=list)

@dataclass
class Work:
    name: str = "" # Company
    position: str = ""
    url: str = ""
    startDate: str = ""
    endDate: str = ""
    summary: str = ""
    highlights: List[str] = field(default_factory=list)

@dataclass
class Education:
    institution: str = ""
    url: str = ""
    area: str = ""
    studyType: str = ""
    startDate: str = ""
    endDate: str = ""
    score: str = ""
    courses: List[str] = field(default_factory=list)

@dataclass
class Skill:
    name: str = ""
    level: str = ""
    keywords: List[str] = field(default_factory=list)

@dataclass
class ResumeData:
    basics: Basics = field(default_factory=Basics)
    work: List[Work] = field(default_factory=list)
    education: List[Education] = field(default_factory=list)
    skills: List[Skill] = field(default_factory=list)
    
    # Custom sections for extensibility
    custom: Dict = field(default_factory=dict)

    def to_dict(self):
        # Helper to convert to dictionary for JSON serialization
        # In a real scenario, use a library like dataclasses-json
        return {
            "basics": self.basics.__dict__,
            "work": [w.__dict__ for w in self.work],
            "education": [e.__dict__ for e in self.education],
            "skills": [s.__dict__ for s in self.skills]
        }
