from datetime import date

from pydantic import BaseModel, field_serializer


class Holder(BaseModel):
    name: str
    shares: float
    reported: date
    percentageOut: float
    value: float

    @field_serializer("reported")
    def serialize_reported(self, reported: date, _info):
        return reported.strftime("%Y-%m-%d")


class HoldersResponse(BaseModel):
    institutionalHolders: list[Holder]
    mutualFundHolders: list[Holder]
