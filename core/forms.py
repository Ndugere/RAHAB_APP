from django import forms
from django.forms import inlineformset_factory
from .models import Account, ReportTag, JournalEntry, JournalLine

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

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ["date", "memo", "posted"]

class JournalLineForm(forms.ModelForm):
    class Meta:
        model = JournalLine
        fields = ["account", "debit", "credit"]

    def clean(self):
        cleaned_data = super().clean()
        debit = cleaned_data.get("debit") or 0
        credit = cleaned_data.get("credit") or 0
        if debit > 0 and credit > 0:
            raise forms.ValidationError("A line cannot have both debit and credit amounts.")
        if debit == 0 and credit == 0:
            raise forms.ValidationError("A line must have either a debit or a credit amount.")
        return cleaned_data

JournalLineFormSet = inlineformset_factory(
    JournalEntry,
    JournalLine,
    form=JournalLineForm,
    extra=2,
    can_delete=True
)