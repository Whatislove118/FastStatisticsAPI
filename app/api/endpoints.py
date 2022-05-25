from fastapi import APIRouter, Body, Depends

from app.api import deps
from app.db import DBManager
from app.models import Statistics
from app.schemas import StatisticsCreate, StatisticsDetails, StrictDate

router = APIRouter()


@router.post("/", response_model=StatisticsDetails)
async def create_statistics(
    db_manager: DBManager = Depends(deps.get_statistics_manager),
    obj_in: StatisticsCreate = Body(...),
):
    """
    Endpoint for creating statistic object

    Params:
    - event_date: Date - date in format YYYY-MM-DD
    - costs: decimal - decimal value in format x.xx

    Return created object
    """
    obj = await db_manager.create(obj_in.dict())
    return obj


@router.get("/", response_model=list[StatisticsDetails])
async def list_statistics(
    from_date: str | StrictDate = None,
    to_date: str | StrictDate = None,
    db_manager: DBManager = Depends(deps.get_statistics_manager),
    order_by: str | None = None,
):
    """
    Endpoint for getting statistics objects

    Query params:
    - from_date: Date - get statistics which event_date greater/equal than from_date value.
                 Pass in format YYYY-MM-DD
    - to_date: Date - get statistics which event_date lower/equal than from_date value.
                 Pass in format YYYY-MM-DD
    - order_by: str - order_by field name. User "-" prefix to use descending ordering.

    Return list of objects
    """

    def filter_statement(query):  # noqa
        if from_date:
            query = query.where(from_date <= Statistics.event_date)
        if to_date:
            query = query.where(to_date >= Statistics.event_date)
        return query

    objects = await db_manager.list(filter_statement, order_by=order_by)
    return objects


@router.delete("/")
async def clear_statistics(
    db_manager: DBManager = Depends(deps.get_statistics_manager),
):
    """
    Endpoint for clearing statistics
    """
    await db_manager.clear()
    return {"detail": "Deleted"}
