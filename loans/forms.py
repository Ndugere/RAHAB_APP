from django import forms
from .models import LoanProduct, Loan

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



# Start of the Loan form

class LoanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Force blank choices for dropdowns so user must select
        self.fields['member'].empty_label = "Select member"
        self.fields['product'].empty_label = "Select loan product"
        self.fields['principal_account'].empty_label = "Select principal account"
        self.fields['interest_account'].empty_label = "Select interest account"

        # Placeholders for better UX
        self.fields['principal'].widget.attrs.update({"placeholder": "e.g. 50000"})
        self.fields['annual_rate'].widget.attrs.update({"placeholder": "e.g. 12.5"})
        self.fields['tenor_months'].widget.attrs.update({"placeholder": "e.g. 12"})

    class Meta:
        model = Loan
        fields = [
            "member",
            "product",
            "principal",
            "annual_rate",
            "interest_method",
            "disbursed_on",
            "tenor_months",
            "status",
            "principal_account",
            "interest_account",
        ]
        labels = {
            "member": "Member",
            "product": "Loan Product",
            "principal": "Principal Amount",
            "annual_rate": "Annual Interest Rate (%)",
            "interest_method": "Interest Calculation Method",
            "disbursed_on": "Disbursement Date",
            "tenor_months": "Tenor (Months)",
            "status": "Loan Status",
            "principal_account": "Principal GL Account",
            "interest_account": "Interest GL Account",
        }
        widgets = {
            "member": forms.Select(attrs={"class": "form-select"}),
            "product": forms.Select(attrs={"class": "form-select"}),
            "principal": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "annual_rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "interest_method": forms.Select(attrs={"class": "form-select"}),
            "disbursed_on": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "tenor_months": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "principal_account": forms.Select(attrs={"class": "form-select"}),
            "interest_account": forms.Select(attrs={"class": "form-select"}),
        }
