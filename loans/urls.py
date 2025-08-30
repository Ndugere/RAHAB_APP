from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.loanproduct_list, name="loanproduct_list"),
    path("products/new/", views.loanproduct_create, name="loanproduct_create"),
    path("<int:pk>/edit/", views.loanproduct_edit, name="loanproduct_edit"),
    path("<int:pk>/delete/", views.loanproduct_delete, name="loanproduct_delete"),

    path("loans/", views.loan_list, name="loan_list"),
    path("loans/new/", views.loan_create, name="loan_create"),
    path("loans/<int:pk>/", views.loan_detail, name="loan_detail"),
    path("loans/<int:pk>/edit/", views.loan_update, name="loan_update"),
    path("loans/<int:pk>/delete/", views.loan_delete, name="loan_delete"),


    # LoanSchedule CRUD
    path("schedules/", views.LoanScheduleListView.as_view(), name="loanschedule_list"),
    path("schedules/add/", views.LoanScheduleCreateView.as_view(), name="loanschedule_add"),
    path("schedules/<int:pk>/edit/", views.LoanScheduleUpdateView.as_view(), name="loanschedule_edit"),
    path("schedules/<int:pk>/delete/", views.LoanScheduleDeleteView.as_view(), name="loanschedule_delete"),

    # Optional nested create under a specific loan
    path("loans/<int:loan_id>/schedules/add/", views.LoanScheduleCreateForLoanView.as_view(),
         name="loanschedule_add_for_loan"),


    path("repayments/", views.LoanRepaymentListView.as_view(), name="loanrepayment_list"),
    path("repayments/add/", views.LoanRepaymentCreateView.as_view(), name="loanrepayment_add"),
    path("repayments/<int:pk>/edit/", views.LoanRepaymentUpdateView.as_view(), name="loanrepayment_edit"),
    path("repayments/<int:pk>/delete/", views.LoanRepaymentDeleteView.as_view(), name="loanrepayment_delete"),
]



