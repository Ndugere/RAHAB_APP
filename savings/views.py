from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import SavingsAccount, SavingsTransaction
from .forms import SavingsAccountForm, SavingsTransactionForm

# Savings Account Views
class SavingsAccountListView(ListView):
    model = SavingsAccount
    template_name = "savings/savingsaccount_list.html"
    context_object_name = "accounts"


class SavingsAccountCreateView(CreateView):
    model = SavingsAccount
    form_class = SavingsAccountForm
    template_name = "savings/savingsaccount_form.html"
    success_url = reverse_lazy("savingsaccount_list")


class SavingsAccountUpdateView(UpdateView):
    model = SavingsAccount
    form_class = SavingsAccountForm
    template_name = "savings/savingsaccount_form.html"
    success_url = reverse_lazy("savingsaccount_list")


class SavingsAccountDeleteView(DeleteView):
    model = SavingsAccount
    template_name = "savings/savingsaccount_confirm_delete.html"
    success_url = reverse_lazy("savingsaccount_list")


# Savings Transaction Views
class SavingsTransactionListView(ListView):
    model = SavingsTransaction
    template_name = "savings/savingstransaction_list.html"
    context_object_name = "transactions"


class SavingsTransactionCreateView(CreateView):
    model = SavingsTransaction
    form_class = SavingsTransactionForm
    template_name = "savings/savingstransaction_form.html"
    success_url = reverse_lazy("savingstransaction_list")


class SavingsTransactionUpdateView(UpdateView):
    model = SavingsTransaction
    form_class = SavingsTransactionForm
    template_name = "savings/savingstransaction_form.html"
    success_url = reverse_lazy("savingstransaction_list")


class SavingsTransactionDeleteView(DeleteView):
    model = SavingsTransaction
    template_name = "savings/savingstransaction_confirm_delete.html"
    success_url = reverse_lazy("savingstransaction_list")
