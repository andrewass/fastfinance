from pydantic import BaseModel


class Profile(BaseModel):
    companyName: str
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
