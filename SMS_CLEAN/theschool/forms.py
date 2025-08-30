from django import forms
from .models import Student, ParentDetails, GuardianDetails

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender',
            'religion', 'grade', 'stream', 'passport_photo'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class ParentDetailsForm(forms.ModelForm):
    class Meta:
        model = ParentDetails
        fields = [
            'father_name', 'father_phone', 'father_occupation',
            'mother_name', 'mother_phone', 'mother_occupation'
        ]

class GuardianDetailsForm(forms.ModelForm):
    class Meta:
        model = GuardianDetails
        fields = ['full_name', 'phone', 'occupation']
