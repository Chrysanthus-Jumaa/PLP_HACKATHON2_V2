from django import template

register = template.Library()

# ----------------------------
# Simple Tags
# ----------------------------

@register.simple_tag
def school_count():
    from theschool.models import School
    return School.objects.count()

@register.simple_tag
def student_count(school_id):
    from theschool.models import Student
    return Student.objects.filter(school_id=school_id).count()

@register.simple_tag
def teacher_count(school_id):
    from theschool.models import Teacher
    return Teacher.objects.filter(school_id=school_id).count()

# ----------------------------
# Custom Filters
# ----------------------------

@register.filter
def dict_get(dictionary, key):
    return dictionary.get(key)
