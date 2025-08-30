from django import forms
from .models import LoanProduct

class LoanProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Force a blank choice at the top for interest_method
        self.fields['interest_method'].choices = [
            ("", "Select interest method")
        ] + list(self.fields['interest_method'].choices)

        # Optional: autofocus first field for faster data entry
        self.fields['name'].widget.attrs.update({
            "placeholder": "e.g. Development Loan",
            "autofocus": "autofocus"
        })
        self.fields['annual_rate'].widget.attrs.update({
            "placeholder": "e.g. 12.5"
        })
        self.fields['default_tenor_months'].widget.attrs.update({
            "placeholder": "e.g. 12"
        })

    class Meta:
        model = LoanProduct
        fields = [
            "name",
            "description",
            "annual_rate",
            "interest_method",
            "default_tenor_months",
        ]
        labels = {
            "name": "Loan Product Name",
            "description": "Description / Notes",
            "annual_rate": "Annual Interest Rate (%)",
            "interest_method": "Interest Calculation Method",
            "default_tenor_months": "Default Tenor (Months)",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "annual_rate": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0"
            }),
            "interest_method": forms.Select(attrs={"class": "form-select"}),
            "default_tenor_months": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1
            }),
        }
