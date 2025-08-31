from django import forms
from .models import Receipt

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = [
            "type",
            "amount",
            "payment_method",
            "reference_note",
        ]
        widgets = {
            "type": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "payment_method": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Mobile, Cash, Bank"}),
            "reference_note": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Optional notes"}),
        }
