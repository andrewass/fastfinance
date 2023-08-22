from datetime import date
from pydantic import BaseModel


class Holder(BaseModel):
    name: str
    shares: float
    dateReported: date
    percentageOut: float
    value: float


class HoldersDetails(BaseModel):
    institutionalHolders: list[Holder]
    mutualFundHolders: list[Holder]
