from dataclasses import dataclass
from math import floor


@dataclass(frozen=True)
class AttendanceSnapshot:
    attended: int
    total: int
    minimum_percent: float = 75.0

    def __post_init__(self) -> None:
        if self.attended < 0:
            raise ValueError("attended must be non-negative")
        if self.total < 0:
            raise ValueError("total must be non-negative")
        if self.attended > self.total:
            raise ValueError("attended cannot exceed total")
        if not 0 < self.minimum_percent < 100:
            raise ValueError("minimum_percent must be greater than 0 and less than 100")

    @property
    def percent(self) -> float:
        return 100.0 if self.total == 0 else round(self.attended / self.total * 100, 2)


def safe_skip_count(snapshot: AttendanceSnapshot) -> int:
    skips = 0
    attended = snapshot.attended
    total = snapshot.total
    while total + 1 > 0 and attended / (total + 1) * 100 >= snapshot.minimum_percent:
        skips += 1
        total += 1
    return skips


def classes_needed_for_safety(snapshot: AttendanceSnapshot) -> int:
    if snapshot.percent >= snapshot.minimum_percent:
        return 0
    required = (snapshot.minimum_percent * snapshot.total - 100 * snapshot.attended) / (100 - snapshot.minimum_percent)
    return max(0, floor(required) + 1)


def attendance_recommendation(snapshot: AttendanceSnapshot) -> dict[str, object]:
    skips = safe_skip_count(snapshot)
    needed = classes_needed_for_safety(snapshot)
    if needed > 0:
        action = "attend"
        reason = f"Attend at least {needed} upcoming classes to recover above {snapshot.minimum_percent}%."
    elif skips == 0:
        action = "attend"
        reason = "You are at the threshold; skipping would create attendance risk."
    else:
        action = "flexible"
        reason = f"You can safely skip {skips} class(es) if deadlines or health require it."
    return {"action": action, "reason": reason, "safe_skip_count": skips, "classes_needed": needed}
