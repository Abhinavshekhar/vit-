from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass(frozen=True)
class TaskInput:
    id: str
    title: str
    priority: int
    deadline: datetime
    duration_minutes: int
    difficulty: int = 3
    energy_required: int = 3
    dependencies: list[str] = field(default_factory=list)
    preferred_start_hour: int | None = None

    def __post_init__(self) -> None:
        if not 1 <= self.priority <= 100:
            raise ValueError("priority must be between 1 and 100")
        if self.duration_minutes <= 0:
            raise ValueError("duration_minutes must be positive")
        if not 1 <= self.difficulty <= 5:
            raise ValueError("difficulty must be between 1 and 5")
        if not 1 <= self.energy_required <= 5:
            raise ValueError("energy_required must be between 1 and 5")
        if self.preferred_start_hour is not None and not 0 <= self.preferred_start_hour <= 23:
            raise ValueError("preferred_start_hour must be between 0 and 23")


@dataclass(frozen=True)
class BusyBlock:
    title: str
    start: datetime
    end: datetime
    fixed: bool = True


@dataclass(frozen=True)
class ScheduleRequest:
    day_start: datetime
    day_end: datetime
    tasks: list[TaskInput]
    busy: list[BusyBlock] = field(default_factory=list)
    energy_by_hour: dict[int, int] = field(default_factory=dict)


@dataclass(frozen=True)
class ScheduleBlock:
    task_id: str
    title: str
    start: datetime
    end: datetime
    score: float


@dataclass(frozen=True)
class ScheduleResponse:
    blocks: list[ScheduleBlock]
    unscheduled_task_ids: list[str]
    conflicts: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "blocks": [
                {
                    "task_id": block.task_id,
                    "title": block.title,
                    "start": block.start.isoformat(),
                    "end": block.end.isoformat(),
                    "score": block.score,
                }
                for block in self.blocks
            ],
            "unscheduled_task_ids": self.unscheduled_task_ids,
            "conflicts": self.conflicts,
        }


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


def _dependencies_satisfied(task: TaskInput, completed: set[str]) -> bool:
    return all(dep in completed for dep in task.dependencies)


def build_schedule(request: ScheduleRequest) -> ScheduleResponse:
    if request.day_end <= request.day_start:
        raise ValueError("day_end must be after day_start")

    scheduled: list[ScheduleBlock] = []
    unscheduled: list[str] = []
    conflicts: list[str] = []
    completed: set[str] = set()
    remaining = sorted(request.tasks, key=lambda t: (-t.priority, t.deadline, -t.difficulty))

    progress = True
    while remaining and progress:
        progress = False
        next_round: list[TaskInput] = []
        for task in remaining:
            if not _dependencies_satisfied(task, completed):
                next_round.append(task)
                continue

            best: tuple[float, datetime] | None = None
            cursor = request.day_start
            latest_end = min(request.day_end, task.deadline)
            while cursor + timedelta(minutes=task.duration_minutes) <= latest_end:
                end = cursor + timedelta(minutes=task.duration_minutes)
                if not _overlaps(cursor, end, [*request.busy, *scheduled]):
                    score = _candidate_score(task, cursor, request)
                    if best is None or score > best[0]:
                        best = (score, cursor)
                cursor += timedelta(minutes=15)

            if best is None:
                unscheduled.append(task.id)
                conflicts.append(f"No feasible slot for {task.title} before {task.deadline.isoformat()}.")
                progress = True
                continue

            score, start = best
            scheduled.append(
                ScheduleBlock(
                    task_id=task.id,
                    title=task.title,
                    start=start,
                    end=start + timedelta(minutes=task.duration_minutes),
                    score=round(score, 2),
                )
            )
            completed.add(task.id)
            progress = True
        remaining = next_round

    for task in remaining:
        unscheduled.append(task.id)
        conflicts.append(f"Task {task.id} waits for dependencies {task.dependencies}.")

    return ScheduleResponse(
        blocks=sorted(scheduled, key=lambda b: b.start),
        unscheduled_task_ids=unscheduled,
        conflicts=conflicts,
    )
