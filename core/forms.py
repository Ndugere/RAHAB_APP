from django import forms
from .models import Account, ReportTag

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["code", "name", "type", "parent", "report_tag"]
        widgets = {
            "code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter account code (e.g. 101)",
                "autocomplete": "off"
            }),
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Account name (e.g. Cash on Hand)",
                "autocomplete": "off"
            }),
            "type": forms.Select(attrs={
                "class": "form-select"
            }),
            "parent": forms.Select(attrs={
                "class": "form-select"
            }),
            "report_tag": forms.Select(attrs={
                "class": "form-select"
            }),
        }
        labels = {
            "code": "Account Code",
            "name": "Account Name",
            "type": "Account Type",
            "parent": "Parent Account",
            "report_tag": "Report Tag"
        }
        help_texts = {
            "code": "Unique identifier for the account.",
            "type": "Choose the category this account belongs to.",
            "parent": "Select a parent account if applicable.",
            "report_tag": "Used to classify accounts for financial reporting."
        }
