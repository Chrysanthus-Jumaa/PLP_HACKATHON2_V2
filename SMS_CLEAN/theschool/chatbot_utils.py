# theschool/chatbot_utils.py
from django.db.models import Sum
from .models import Student, FeeRecord, Teacher

def get_chatbot_reply(message: str, user) -> str:
    """
    Simple admin chatbot responder. Supports:
      - "total students" / "how many students"
      - "total teachers"
      - "balance <ADM_NO>"
      - "attendance"  (returns weekly average if available)
    Falls back to a friendly help message.
    """
    msg = (message or "").lower().strip()

    # totals
    if "total students" in msg or "how many students" in msg:
        try:
            # if your Student model has a school FK, filter by user.school
            count = Student.objects.filter(school=user.school).count()
        except Exception:
            count = Student.objects.count()
        return f"There are {count} students registered."

    if "total teachers" in msg or "how many teachers" in msg:
        try:
            count = Teacher.objects.filter(school=user.school).count()
        except Exception:
            count = Teacher.objects.count()
        return f"There are {count} teachers."

    # balance by admission number: "balance ADM123"
    if msg.startswith("balance"):
        parts = msg.split()
        if len(parts) >= 2:
            adm = parts[1].strip()
            try:
                s = Student.objects.get(admission_no__iexact=adm)
            except Student.DoesNotExist:
                return "Student not found. Please check the admission number."
            paid = FeeRecord.objects.filter(student=s).aggregate(total=Sum('amount'))['total'] or 0
            return f"{s.name} (ADM: {s.admission_no}) has paid KES {paid:.2f} so far."
        else:
            return "Please provide an admission number, e.g. 'balance ADM123'."

    # attendance quick answer — try to use Attendance model or precomputed stat
    if "attendance" in msg:
        # attempt to import a simple helper to compute weekly attendance, otherwise fallback
        try:
            from .stats_utils import weekly_attendance_for_school
            stats = weekly_attendance_for_school(user.school)
            wa = stats.get("weekly_attendance_avg", 0)
            return f"Weekly attendance average is {wa:.1f}%."
        except Exception:
            return "Attendance data not available via the chatbot right now."

    # default
    return "I can answer: 'total students', 'total teachers', 'attendance', or 'balance <ADM_NO>'."
