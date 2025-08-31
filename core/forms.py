from django import forms
from django.forms import inlineformset_factory
from .models import Account, ReportTag, JournalEntry, JournalLine, Member


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
        fields = ["date", "reference", "memo", "posted"]  # include reference here
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",  # HTML5 date picker
                    "class": "form-control",
                }
            ),
            "reference": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Reference number or code (e.g. JV-2025-001)"
            }),
            "memo": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Optional memo or description"
            }),
            "posted": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }
        labels = {
            "date": "Entry Date",
            "reference": "Reference",
            "memo": "Memo",
            "posted": "Mark as Posted"
        }
        help_texts = {
            "reference": "Short code or number for this journal entry (e.g. voucher number).",
            "memo": "Brief description of the transaction."
        }



class JournalLineForm(forms.ModelForm):
    class Meta:
        model = JournalLine
        fields = ["account", "debit", "credit"]
        widgets = {
            "account": forms.Select(attrs={
                "class": "form-select",
                "title": "Select the account affected by this line"
            }),
            "debit": forms.NumberInput(attrs={
                "class": "form-control text-end",
                "placeholder": "0.00",
                "step": "0.01",
                "min": "0"
            }),
            "credit": forms.NumberInput(attrs={
                "class": "form-control text-end",
                "placeholder": "0.00",
                "step": "0.01",
                "min": "0"
            }),
        }
        labels = {
            "account": "Account",
            "debit": "Debit Amount",
            "credit": "Credit Amount"
        }
        help_texts = {
            "debit": "Enter an amount here only if this is a debit.",
            "credit": "Enter an amount here only if this is a credit."
        }

    def clean(self):
        cleaned_data = super().clean()
        debit = cleaned_data.get("debit") or 0
        credit = cleaned_data.get("credit") or 0

        if debit > 0 and credit > 0:
            raise forms.ValidationError(
                "This line has both a debit and a credit. Please enter an amount in only one column."
            )
        if debit == 0 and credit == 0:
            raise forms.ValidationError(
                "This line is empty. Please enter a debit or a credit amount."
            )

        return cleaned_data


# Inline formset for Journal Lines
JournalLineFormSet = inlineformset_factory(
    JournalEntry,
    JournalLine,
    form=JournalLineForm,
    extra=2,          # number of blank lines shown by default
    can_delete=True   # allow removing lines
)



class MemberForm(forms.ModelForm):
    """
    Professional-grade form for creating and updating SACCO members.
    Includes Bootstrap styling, placeholders, and consistent UX patterns.
    """

    class Meta:
        model = Member
        fields = [
            "member_no",
            "payroll_number",  # 👈 Added field
            "full_name",
            "id_number",
            "phone",
            "email",
            "address",
            "joined_on",
            "status",
            "notes",
        ]
        widgets = {
            "member_no": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. M-2025-001",
                "autocomplete": "off"
            }),
            "payroll_number": forms.TextInput(attrs={  # 👈 New widget
                "class": "form-control",
                "placeholder": "e.g. PR-45678",
                "autocomplete": "off"
            }),
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Full legal name"
            }),
            "id_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "National ID or Passport No."
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. +254712345678"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "name@example.com"
            }),
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Residential or postal address"
            }),
            "joined_on": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "status": forms.Select(attrs={
                "class": "form-select"
            }),
            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Additional remarks or notes"
            }),
        }

    def clean_member_no(self):
        member_no = self.cleaned_data.get("member_no", "").strip().upper()
        if not member_no:
            raise forms.ValidationError("Member number is required.")
        return member_no

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if phone and not phone.startswith("+"):
            raise forms.ValidationError("Phone number must include country code, e.g. +254...")
        return phone
