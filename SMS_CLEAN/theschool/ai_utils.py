# theschool/ai_utils.py
from statistics import mean

def generate_insight(stats: dict) -> dict:
    """
    Accepts a stats dict and returns a short insight + suggested actions.
    Stats expected keys (if available):
      total_students, total_teachers, boys, girls,
      mon, tue, wed, thu, fri (attendance % numbers 0-100),
      weekly_attendance_avg, fee_collection_rate (0-100)
    Returns {"message": str, "actions": [str,...]}
    """
    msgs = []
    actions = []

    wa = stats.get("weekly_attendance_avg")
    if wa is not None:
        if wa < 70:
            msgs.append(f"Attendance is low ({wa:.0f}%). Consider parent outreach and follow-ups.")
            actions.append("send_attendance_reminder")
        elif wa < 85:
            msgs.append(f"Attendance moderate ({wa:.0f}%). Continue monitoring.")
        else:
            msgs.append(f"Attendance looks healthy ({wa:.0f}%). Great job!")

    # weekly trend
    days = [stats.get(k) for k in ("mon", "tue", "wed", "thu", "fri")]
    if all(isinstance(d, (int, float)) for d in days):
        slope = (days[-1] - days[0]) / 4.0
        if slope > 2:
            msgs.append("Attendance is trending up through the week.")
        elif slope < -2:
            msgs.append("Attendance is falling through the week — investigate causes.")
        else:
            msgs.append("Attendance is stable across the week.")

    # gender balance
    boys = stats.get("boys", 0) or 0
    girls = stats.get("girls", 0) or 0
    total = boys + girls
    if total > 0:
        pct_boys = boys * 100.0 / total
        if pct_boys > 65:
            msgs.append(f"Gender imbalance: {pct_boys:.0f}% boys — consider targeted outreach to girls.")
        elif pct_boys < 35:
            msgs.append(f"Gender imbalance: {100-pct_boys:.0f}% girls — consider outreach to boys.")

    # fee collection
    fcr = stats.get("fee_collection_rate")
    if isinstance(fcr, (int, float)):
        if fcr < 70:
            msgs.append(f"Fee collection is low ({fcr:.0f}%). Consider sending payment reminders.")
            actions.append("send_fee_reminder")

    message = " ".join(msgs).strip()
    if not message:
        message = "No strong signals found — metrics look stable."

    # limit length
    if len(message) > 400:
        message = message[:397] + "..."

    return {"message": message, "actions": actions}
