import uuid

from sqlalchemy import DECIMAL, CheckConstraint, Column, Date, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property

from app.db.base_class import Base


class Statistics(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    event_date = Column(Date, nullable=False)
    views = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    cost = Column(DECIMAL(20, 2), default=0.00)

    @hybrid_property
    def cpc(self) -> float:
        try:
            return self.cost / self.clicks
        except Exception:  # cause pydantic can catch only BaseExceptions
            return 0.00

    @hybrid_property
    def cpm(self) -> float:
        try:
            return self.cost / self.views * 1000
        except Exception:  # cause pydantic can catch only BaseExceptions
            return 0.00

    __table_args__ = (
        CheckConstraint(views >= 0, name="check_views_positive"),
        CheckConstraint(clicks >= 0, name="check_clicks_positive"),
        CheckConstraint(cost >= 0.00, name="check_cost_positive"),
    )
