from django import forms

class EmployeeForm(forms.Form):
    emp_id = forms.CharField(required=True)
    fullname = forms.CharField(required=True)
    asset_tag = forms.CharField(required=True)
    duration = forms.CharField(required=False)  # Duration may not be required for returns

    form_type = forms.ChoiceField(choices=[('borrow', 'Borrow'), ('return', 'Return')], required=True)
