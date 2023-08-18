from dataclasses import dataclass
from datetime import date


@dataclass
class Holder:
    name: str
    shares: float
    dateReported: date
    percentageOut: float
    value: float


@dataclass
class HoldersDetails:
    institutionalHolders: list[Holder]
    mutualFundHolders: list[Holder]
