from django import forms
from .models import CustomUser, Calculation


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username',  'email', 'password']


class CalculationForm(forms.ModelForm):
    class Meta:
        model = Calculation
        fields = ['num1', 'num2', 'operation']

class OperationSelectionForm(forms.Form):
    OPERATION_CHOICES = [
        ("add", "Addition"),
        ("sub", "Subtraction"),
        ("multi", "Multiplication"),
        ("div", "Division"),
    ]
    operation = forms.ChoiceField(choices=OPERATION_CHOICES, label="Select Operation")