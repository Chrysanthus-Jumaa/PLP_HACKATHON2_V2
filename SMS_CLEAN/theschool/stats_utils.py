# theschool/stats_utils.py
from datetime import date, timedelta

def _week_dates(reference=None):
    """Return Monday..Friday dates for week containing reference (or today)."""
    if reference is None:
        reference = date.today()
    monday = reference - timedelta(days=reference.weekday())  # Monday
    return [monday + timedelta(days=i) for i in range(5)]

def weekly_attendance_for_school(school):
    """
    Attempts to compute attendance % for Mon..Fri and weekly average.
    This expects you to have an Attendance model with:
      - date (date)
      - present (bool)
      - student (FK) or school (FK)
    If no compatible model exists, returns zeros.
    """
    try:
        # Import late to avoid circular imports
        from .models import Attendance  # adapt name if different
    except Exception:
        # Attendance model not found — return zeros
        return {"mon": 0, "tue": 0, "wed": 0, "thu": 0, "fri": 0, "weekly_attendance_avg": 0}

    dates = _week_dates()
    day_keys = ["mon", "tue", "wed", "thu", "fri"]
    results = {}
    percents = []
    for key, day in zip(day_keys, dates):
        # try multiple possible filters: if Attendance has school FK or student FK
        qs = Attendance.objects.filter(date=day)
        if hasattr(Attendance, "school_id"):
            qs = qs.filter(school=school)
        elif hasattr(Attendance, "student_id"):
            # try students belonging to school
            qs = qs.filter(student__school=school)
        total = qs.count()
        if total == 0:
            pct = 0
        else:
            present = qs.filter(present=True).count()
            pct = (present / total) * 100.0
        results[key] = round(pct, 1)
        percents.append(pct)
    results["weekly_attendance_avg"] = round(sum(percents) / len(percents), 1) if percents else 0
    return results
