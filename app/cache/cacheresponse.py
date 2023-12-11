from datetime import datetime

from pydantic import BaseModel, field_serializer


class CacheResponse(BaseModel):
    added: datetime
    data: dict

    @field_serializer("added")
    def serialize_data(self, added: datetime, _info):
        return added.timestamp()
