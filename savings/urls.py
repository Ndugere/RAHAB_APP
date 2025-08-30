from django.urls import path
from . import views

urlpatterns = [
    # Savings Accounts
    path("accounts/", views.SavingsAccountListView.as_view(), name="savingsaccount_list"),
    path("accounts/add/", views.SavingsAccountCreateView.as_view(), name="savingsaccount_add"),
    path("accounts/<int:pk>/edit/", views.SavingsAccountUpdateView.as_view(), name="savingsaccount_edit"),
    path("accounts/<int:pk>/delete/", views.SavingsAccountDeleteView.as_view(), name="savingsaccount_delete"),

    # Savings Transactions
    path("transactions/", views.SavingsTransactionListView.as_view(), name="savingstransaction_list"),
    path("transactions/add/", views.SavingsTransactionCreateView.as_view(), name="savingstransaction_add"),
    path("transactions/<int:pk>/edit/", views.SavingsTransactionUpdateView.as_view(), name="savingstransaction_edit"),
    path("transactions/<int:pk>/delete/", views.SavingsTransactionDeleteView.as_view(), name="savingstransaction_delete"),
]
