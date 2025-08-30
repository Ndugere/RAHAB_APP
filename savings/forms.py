from django import forms
from .models import SavingsAccount, SavingsTransaction

class SavingsAccountForm(forms.ModelForm):
    class Meta:
        model = SavingsAccount
        fields = ['member', 'account', 'opened_on', 'active']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'account': forms.Select(attrs={'class': 'form-select'}),
            'opened_on': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SavingsTransactionForm(forms.ModelForm):
    class Meta:
        model = SavingsTransaction
        fields = ['savings_account', 'date', 'transaction_type', 'amount', 'journal_entry', 'notes']
        widgets = {
            'savings_account': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'journal_entry': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.TextInput(attrs={'class': 'form-control'}),
        }
