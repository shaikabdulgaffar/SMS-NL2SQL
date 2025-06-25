from django import forms
from .models import Student, Department
import re

INDIAN_STATES = [
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
    ('Chandigarh', 'Chandigarh'),
    ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('Delhi', 'Delhi'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Ladakh', 'Ladakh'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Puducherry', 'Puducherry'),
]

class StudentForm(forms.ModelForm):
    state = forms.ChoiceField(choices=INDIAN_STATES)
    country = forms.ChoiceField(choices=[('India', 'India')])
    present_department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Select Department")

    class Meta:
        model = Student
        exclude = ['admission_number']  # Hide admission_number from form

    def clean_parent_mobile(self):
        value = self.cleaned_data.get('parent_mobile')
        if value and not re.fullmatch(r'\d{10,15}', value):
            raise forms.ValidationError("Parent mobile must be numeric and 10-15 digits.")
        return value

    def clean_student_mobile(self):
        value = self.cleaned_data.get('student_mobile')
        if value and not re.fullmatch(r'\d{10,15}', value):
            raise forms.ValidationError("Student mobile must be numeric and 10-15 digits.")
        return value

    def clean_tenth_marks(self):
        value = self.cleaned_data.get('tenth_marks')
        if value is not None and value < 0:
            raise forms.ValidationError("Marks must be a positive number.")
        return value

    def clean_twelfth_marks(self):
        value = self.cleaned_data.get('twelfth_marks')
        if value is not None and value < 0:
            raise forms.ValidationError("Marks must be a positive number.")
        return value

    def clean_degree_marks(self):
        value = self.cleaned_data.get('degree_marks')
        if value is not None and value < 0:
            raise forms.ValidationError("Marks must be a positive number.")
        return value

    def clean_total_fees(self):
        value = self.cleaned_data.get('total_fees')
        if value is not None and value < 0:
            raise forms.ValidationError("Fees must be a positive number.")
        return value

    def clean_paid_fees(self):
        value = self.cleaned_data.get('paid_fees')
        if value is not None and value < 0:
            raise forms.ValidationError("Fees must be a positive number.")
        return value

    def clean_present_department(self):
        dept = self.cleaned_data['present_department']
        # dept is Department object, return its name for CharField
        return dept.name if dept else ''