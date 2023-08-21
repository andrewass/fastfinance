from dataclasses import dataclass


@dataclass
class Profile:
    address: str
    city: str
    state: str
    zip: str
    country: str
    website: str
    industry: str
    sector: str
    businessSummary: str
    fullTimeEmployees: int
