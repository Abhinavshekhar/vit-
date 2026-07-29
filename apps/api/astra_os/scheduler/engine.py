from datetime import datetime, timedelta
from pydantic import BaseModel, Field


class TaskInput(BaseModel):
    id: str
    title: str
    priority: int = Field(ge=1, le=100)
    deadline: datetime
    duration_minutes: int = Field(gt=0)
    difficulty: int = Field(ge=1, le=5)
    energy_required: int = Field(ge=1, le=5)
    dependencies: list[str] = Field(default_factory=list)
    preferred_start_hour: int | None = Field(default=None, ge=0, le=23)


class BusyBlock(BaseModel):
    title: str
    start: datetime
    end: datetime
    fixed: bool = True


class ScheduleRequest(BaseModel):
    day_start: datetime
    day_end: datetime
    tasks: list[TaskInput]
    busy: list[BusyBlock] = Field(default_factory=list)
    energy_by_hour: dict[int, int] = Field(default_factory=dict)


class ScheduleBlock(BaseModel):
    task_id: str
    title: str
    start: datetime
    end: datetime
    score: float


class ScheduleResponse(BaseModel):
    blocks: list[ScheduleBlock]
    unscheduled_task_ids: list[str]
    conflicts: list[str]


def _urgency(task: TaskInput, now: datetime) -> float:
    hours = max((task.deadline - now).total_seconds() / 3600, 1)
    return 100 / hours


def _candidate_score(task: TaskInput, start: datetime, request: ScheduleRequest) -> float:
    energy = request.energy_by_hour.get(start.hour, 3)
    energy_fit = 10 - abs(energy - task.energy_required) * 2
    preferred = 5 if task.preferred_start_hour == start.hour else 0
    return task.priority * 2 + task.difficulty * 3 + _urgency(task, request.day_start) + energy_fit + preferred


def _overlaps(start: datetime, end: datetime, blocks: list[BusyBlock | ScheduleBlock]) -> bool:
    return any(start < block.end and end > block.start for block in blocks)


def build_schedule(request: ScheduleRequest) -> ScheduleResponse:
    scheduled: list[ScheduleBlock] = []
    unscheduled: list[str] = []
    conflicts: list[str] = []
    completed: set[str] = set()
    tasks = sorted(request.tasks, key=lambda t: (-t.priority, t.deadline, -t.difficulty))

    for task in tasks:
        if any(dep not in completed for dep in task.dependencies):
            unscheduled.append(task.id)
            conflicts.append(f"Task {task.id} waits for dependencies {task.dependencies}.")
            continue
        best: tuple[float, datetime] | None = None
        cursor = request.day_start
        while cursor + timedelta(minutes=task.duration_minutes) <= min(request.day_end, task.deadline):
            end = cursor + timedelta(minutes=task.duration_minutes)
            if not _overlaps(cursor, end, [*request.busy, *scheduled]):
                score = _candidate_score(task, cursor, request)
                if best is None or score > best[0]:
                    best = (score, cursor)
            cursor += timedelta(minutes=15)
        if best is None:
            unscheduled.append(task.id)
            conflicts.append(f"No feasible slot for {task.title} before {task.deadline.isoformat()}.")
            continue
        score, start = best
        block = ScheduleBlock(
            task_id=task.id,
            title=task.title,
            start=start,
            end=start + timedelta(minutes=task.duration_minutes),
            score=round(score, 2),
        )
        scheduled.append(block)
        completed.add(task.id)
    return ScheduleResponse(blocks=sorted(scheduled, key=lambda b: b.start), unscheduled_task_ids=unscheduled, conflicts=conflicts)
