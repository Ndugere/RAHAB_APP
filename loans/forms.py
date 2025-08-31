from django import forms
from django.core.exceptions import ValidationError
from .models import LoanSchedule, Loan, LoanProduct, LoanRepayment

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





class LoanScheduleForm(forms.ModelForm):
    class Meta:
        model = LoanSchedule
        fields = [
            "loan",
            "installment_no",
            "due_date",
            "principal_due",
            "interest_due",
            "total_due",
            "paid",
        ]
        widgets = {
            "loan": forms.Select(attrs={
                "class": "form-select",
            }),
            "installment_no": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. 1 for first installment"
            }),
            "due_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "principal_due": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter principal amount"
            }),
            "interest_due": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter interest amount"
            }),
            "total_due": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Auto-calculated if left blank"
            }),
            "paid": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }
        labels = {
            "loan": "Loan",
            "installment_no": "Installment Number",
            "due_date": "Due Date",
            "principal_due": "Principal Due",
            "interest_due": "Interest Due",
            "total_due": "Total Due",
            "paid": "Mark as Paid",
        }
        help_texts = {
            "loan": "Select the loan this schedule belongs to.",
            "installment_no": "Unique number for this installment in the loan.",
            "due_date": "Select the due date for this installment.",
            "principal_due": "Amount of principal due for this installment.",
            "interest_due": "Interest amount due for this installment.",
            "total_due": "Will be calculated automatically if left blank.",
            "paid": "Check if this installment has been fully paid.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: filter loans to active ones
        self.fields["loan"].queryset = Loan.objects.all()

    def clean(self):
        cleaned = super().clean()
        principal = cleaned.get("principal_due")
        interest = cleaned.get("interest_due")
        total = cleaned.get("total_due")

        if principal is not None and interest is not None:
            expected = principal + interest
            if total is None:
                cleaned["total_due"] = expected
            elif total != expected:
                raise ValidationError({
                    "total_due": "Total due must equal principal + interest."
                })
        return cleaned

    def clean_installment_no(self):
        inst = self.cleaned_data["installment_no"]
        loan = self.cleaned_data.get("loan") or getattr(self.instance, "loan", None)
        if loan and inst:
            exists = LoanSchedule.objects.filter(loan=loan, installment_no=inst)
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)
            if exists.exists():
                raise ValidationError(
                    "This installment number already exists for the selected loan."
                )
        return inst



class LoanRepaymentForm(forms.ModelForm):
    class Meta:
        model = LoanRepayment
        fields = [
            "loan",
            "date",
            "amount",
            "principal_component",
            "interest_component",
            "journal_entry",
            "source",  # Newly added
            "excess_routed_to_savings",  # Newly added
        ]
        widgets = {
            "loan": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Total repayment amount"}),
            "principal_component": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Principal portion"}),
            "interest_component": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Interest portion"}),
            "journal_entry": forms.Select(attrs={"class": "form-select"}),
            "source": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Mobile, Manual"}),
            "excess_routed_to_savings": forms.NumberInput(attrs={"class": "form-control", "readonly": True}),
        }
        labels = {
            "loan": "Loan",
            "date": "Repayment Date",
            "amount": "Total Amount Paid",
            "principal_component": "Principal Component",
            "interest_component": "Interest Component",
            "journal_entry": "Linked Journal Entry",
            "source": "Repayment Source",
            "excess_routed_to_savings": "Excess Routed to Savings",
        }
        help_texts = {
            "loan": "Select the loan this repayment is for.",
            "amount": "Total amount received from the member.",
            "principal_component": "Part of the payment that reduces the loan principal.",
            "interest_component": "Part of the payment that covers interest.",
            "journal_entry": "Optional: link to the accounting journal entry for this repayment.",
            "source": "Optional tag for repayment origin (e.g. Mobile, Manual, Auto).",
            "excess_routed_to_savings": "Amount redirected to savings due to overpayment.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["loan"].queryset = Loan.objects.all()
        self.fields["source"].required = False
        self.fields["excess_routed_to_savings"].required = False

    def clean(self):
        cleaned = super().clean()
        principal = cleaned.get("principal_component") or 0
        interest = cleaned.get("interest_component") or 0
        amount = cleaned.get("amount") or 0
        loan = cleaned.get("loan")

        if principal + interest > amount:
            raise ValidationError("Principal + Interest cannot exceed the Total Amount Paid.")

        # Auto-calculate excess if loan is provided
        if loan:
            loan_balance = loan.get_balance()
            excess = max(0, amount - loan_balance)
            cleaned["excess_routed_to_savings"] = excess

        return cleaned

