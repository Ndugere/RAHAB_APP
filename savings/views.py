# Django core imports
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


# Local app imports
from .models import SavingsAccount, SavingsTransaction
from .forms import SavingsAccountForm, SavingsTransactionForm

# Cross-app imports
from receipts.models import Receipt

# Savings Account Views
class SavingsAccountListView(LoginRequiredMixin, ListView):
    model = SavingsAccount
    template_name = "savings/savingsaccount_list.html"
    context_object_name = "accounts"


class SavingsAccountCreateView(LoginRequiredMixin, CreateView):
    model = SavingsAccount
    form_class = SavingsAccountForm
    template_name = "savings/savingsaccount_form.html"
    success_url = reverse_lazy("savingsaccount_list")


class SavingsAccountUpdateView(LoginRequiredMixin, UpdateView):
    model = SavingsAccount
    form_class = SavingsAccountForm
    template_name = "savings/savingsaccount_form.html"
    success_url = reverse_lazy("savingsaccount_list")


class SavingsAccountDeleteView(LoginRequiredMixin, DeleteView):
    model = SavingsAccount
    template_name = "savings/savingsaccount_confirm_delete.html"
    success_url = reverse_lazy("savingsaccount_list")


# Savings Transaction Views
class SavingsTransactionListView(LoginRequiredMixin, ListView):
    model = SavingsTransaction
    template_name = "savings/savingstransaction_list.html"
    context_object_name = "transactions"



class SavingsTransactionCreateView(LoginRequiredMixin, CreateView):
    model = SavingsTransaction
    form_class = SavingsTransactionForm
    template_name = "savings/savingstransaction_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        transaction = self.object

        # Only generate receipt for deposits
        if transaction.transaction_type == "DEPOSIT":
            receipt = Receipt.objects.create(
                member=transaction.member,
                type="SAVINGS",
                amount=transaction.amount,
                savings_deposit=transaction,  # assuming this FK exists
                journal_entry=transaction.journal_entry,
                payment_method=transaction.payment_method,
                issued_by=self.request.user,
                reference_note=f"Auto-generated for Savings Deposit #{transaction.id}"
            )

            return redirect(reverse("receipts:receipt_print", kwargs={"pk": receipt.pk}))

        return response  # fallback for withdrawals or other types



class SavingsTransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = SavingsTransaction
    form_class = SavingsTransactionForm
    template_name = "savings/savingstransaction_form.html"
    success_url = reverse_lazy("savingstransaction_list")

class SavingsTransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = SavingsTransaction
    template_name = "savings/savingstransaction_confirm_delete.html"
    success_url = reverse_lazy("savingstransaction_list")
