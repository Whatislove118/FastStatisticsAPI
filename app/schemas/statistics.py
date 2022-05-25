from datetime import date
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel
from pydantic.datetime_parse import get_numeric, parse_date


def validate_date(v: Any) -> date:
    if get_numeric(v, "YYYY-MM-DD") is not None:
        raise ValueError("Don't allow numbers")
    return parse_date(v)


class StrictDate(date):
    @classmethod
    def __get_validators__(cls):
        yield validate_date


class StatisticsCreate(BaseModel):
    event_date: StrictDate
    cost: Decimal = 0.00


class StatisticsDetails(StatisticsCreate):
    id: UUID
    event_date: date
    views: int = 0
    clicks: int = 0
    cpc: Decimal = 0.00
    cpm: Decimal = 0.00

    class Config:
        orm_mode = True
