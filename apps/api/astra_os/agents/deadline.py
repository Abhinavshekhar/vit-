from datetime import date, timedelta
from pydantic import BaseModel, Field


class DeadlineTask(BaseModel):
    title: str
    deadline: date
    estimated_hours: float = Field(gt=0)
    difficulty: int = Field(ge=1, le=5)


class WorkSlice(BaseModel):
    title: str
    planned_date: date
    hours: float


def split_deadline(task: DeadlineTask, today: date) -> list[WorkSlice]:
    latest_work_day = task.deadline - timedelta(days=1)
    if latest_work_day < today:
        return [WorkSlice(title=f"Emergency finish: {task.title}", planned_date=today, hours=task.estimated_hours)]

    days = max(1, (latest_work_day - today).days + 1)
    phases = ["Research", "Draft", "Complete", "Review"]
    hours = round(task.estimated_hours / min(days, len(phases)), 2)
    slices: list[WorkSlice] = []
    for index in range(min(days, len(phases))):
        slices.append(
            WorkSlice(
                title=f"{phases[index]}: {task.title}",
                planned_date=today + timedelta(days=index),
                hours=hours,
            )
        )
    return slices
