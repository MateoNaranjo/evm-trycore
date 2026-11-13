"""Modelos ORM. Deben mantenerse alineados con db/init.sql."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

NAME_MAX_LENGTH = 150
MONEY_TOTAL_DIGITS = 14
PERCENTAGE_TOTAL_DIGITS = 5
DECIMAL_PLACES = 2


class ProjectRecord(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH))
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    activities: Mapped[list["ActivityRecord"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="ActivityRecord.id",
    )


class ActivityRecord(Base):
    __tablename__ = "activities"
    __table_args__ = (
        CheckConstraint("budget_at_completion > 0", name="ck_activities_budget_positive"),
        CheckConstraint(
            "planned_percentage BETWEEN 0 AND 100", name="ck_activities_planned_range"
        ),
        CheckConstraint("actual_percentage BETWEEN 0 AND 100", name="ck_activities_actual_range"),
        CheckConstraint("actual_cost >= 0", name="ck_activities_cost_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH))
    budget_at_completion: Mapped[Decimal] = mapped_column(
        Numeric(MONEY_TOTAL_DIGITS, DECIMAL_PLACES)
    )
    planned_percentage: Mapped[Decimal] = mapped_column(
        Numeric(PERCENTAGE_TOTAL_DIGITS, DECIMAL_PLACES)
    )
    actual_percentage: Mapped[Decimal] = mapped_column(
        Numeric(PERCENTAGE_TOTAL_DIGITS, DECIMAL_PLACES)
    )
    actual_cost: Mapped[Decimal] = mapped_column(Numeric(MONEY_TOTAL_DIGITS, DECIMAL_PLACES))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    project: Mapped[ProjectRecord] = relationship(back_populates="activities")
