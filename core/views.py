from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Account, JournalEntry, Member
from .forms import AccountForm, JournalEntryForm, JournalLineFormSet, MemberForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.db.models import Q
from core.models import Member, MemberTransaction  # adjust paths as needed
from savings.models import SavingsTransaction, SavingsAccount
from loans.models import Loan  # assuming you have a Loan model
from django.db.models import Sum

# -----------------------------
# ACCOUNT VIEWS
# -----------------------------

class MyLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True  # If already logged in, go to dashboard

    def get_success_url(self):
        # Always send to dashboard after login
        return reverse_lazy('dashboard')
    
@login_required
def dashboard(request):
    # Example data for the dashboard
    total_accounts = Account.objects.count()
    total_entries = JournalEntry.objects.count()
    recent_entries = JournalEntry.objects.order_by('-date')[:5]

    context = {
        'total_accounts': total_accounts,
        'total_entries': total_entries,
        'recent_entries': recent_entries,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def account_list(request):
    accounts = Account.objects.all().order_by("code")
    return render(request, "core/account_list.html", {"accounts": accounts})


@login_required
def account_create(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Account created successfully.")
            return redirect("account_list")
    else:
        form = AccountForm()
    return render(request, "core/account_form.html", {"form": form})


@login_required
def account_edit(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Account updated successfully.")
            return redirect("account_list")
    else:
        form = AccountForm(instance=account)
    return render(request, "core/account_form.html", {"form": form})


# -----------------------------
# JOURNAL ENTRY VIEWS
# -----------------------------

@login_required
def journal_entry_list(request):
    entries = JournalEntry.objects.all().order_by("-date", "-id")
    return render(request, "core/journal_entry_list.html", {"entries": entries})


@login_required
@transaction.atomic
def journal_entry_create(request):
    if request.method == "POST":
        form = JournalEntryForm(request.POST)
        formset = JournalLineFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # Sum only non-deleted lines
            total_debit = sum(
                (f.cleaned_data.get("debit") or 0)
                for f in formset
                if not f.cleaned_data.get("DELETE", False)
            )
            total_credit = sum(
                (f.cleaned_data.get("credit") or 0)
                for f in formset
                if not f.cleaned_data.get("DELETE", False)
            )

            if total_debit != total_credit:
                messages.error(request, "⚠️ Total debits must equal total credits.")
            else:
                entry = form.save(commit=False)
                entry.created_by = request.user
                entry.save()
                formset.instance = entry
                formset.save()
                messages.success(request, "✅ Journal entry created successfully.")
                return redirect("journal_entry_list")
        else:
            # Show form and formset errors in console for debugging
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)

    else:
        form = JournalEntryForm()
        formset = JournalLineFormSet()

    return render(
        request,
        "core/journal_entry_form.html",
        {"form": form, "formset": formset}
    )


@login_required
@transaction.atomic
def journal_entry_edit(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk)

    if request.method == "POST":
        form = JournalEntryForm(request.POST, instance=entry)
        formset = JournalLineFormSet(request.POST, instance=entry)

        if form.is_valid() and formset.is_valid():
            total_debit = sum(
                (f.cleaned_data.get("debit") or 0)
                for f in formset
                if not f.cleaned_data.get("DELETE", False)
            )
            total_credit = sum(
                (f.cleaned_data.get("credit") or 0)
                for f in formset
                if not f.cleaned_data.get("DELETE", False)
            )

            if total_debit != total_credit:
                messages.error(request, "⚠️ Total debits must equal total credits.")
            else:
                form.save()
                formset.save()
                messages.success(request, "✅ Journal entry updated successfully.")
                return redirect("journal_entry_list")
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)

    else:
        form = JournalEntryForm(instance=entry)
        formset = JournalLineFormSet(instance=entry)

    return render(
        request,
        "core/journal_entry_form.html",
        {"form": form, "formset": formset}
    )



@login_required
def journal_entry_delete(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk)
    if request.method == "POST":
        entry.delete()
        messages.success(request, "🗑️ Journal entry deleted.")
        return redirect("journal_entry_list")
    return render(request, "core/journal_entry_confirm_delete.html", {"entry": entry})



# -----------------------------
# MEMBER VIEWS
# -----------------------------

@login_required
def member_list(request):
    members = Member.objects.all().order_by("member_no")
    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()

    if search:
        members = members.filter(
            Q(member_no__icontains=search) |
            Q(full_name__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search)
        )

    if status:
        members = members.filter(status=status)

    return render(request, "core/member_list.html", {"members": members})



@login_required
def member_create(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Member added successfully.")
            return redirect("member_list")
    else:
        form = MemberForm()
    return render(request, "core/member_form.html", {"form": form})



@login_required
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)

    # Savings summary
    savings_accounts = member.savingsaccount_set.all()
    savings_transactions = SavingsTransaction.objects.filter(savings_account__member=member)

    total_deposits = savings_transactions.filter(transaction_type='DEPOSIT').aggregate(total=Sum('amount'))['total'] or 0
    total_withdrawals = savings_transactions.filter(transaction_type='WITHDRAWAL').aggregate(total=Sum('amount'))['total'] or 0
    total_interest = savings_transactions.filter(transaction_type='INTEREST').aggregate(total=Sum('amount'))['total'] or 0
    total_interest = savings_transactions.filter(transaction_type='INTEREST').aggregate(total=Sum('amount'))['total'] or 0
    savings_balance = total_deposits + total_interest - total_withdrawals

    # Loan summary
    loans = member.loan_set.all()
    total_loan_principal = loans.aggregate(total=Sum('principal'))['total'] or 0
    total_loan_balance = sum(loan.get_balance() for loan in loans)

    # Unified ledger
    member_transactions = member.transactions.all()  # Already ordered by Meta

    # Recent activity
    recent_savings = savings_transactions.order_by('-date', '-id')[:5]
    recent_loans = loans.order_by('-disbursed_on')[:5]
    recent_ledger = member_transactions[:10]

    net_position = savings_balance - total_loan_balance
    loan_to_savings_ratio = total_loan_balance / savings_balance if savings_balance > 0 else None



    context = {

        "member": member,
        "savings_balance": savings_balance,
        "total_deposits": total_deposits,
        "total_withdrawals": total_withdrawals,
        "total_interest": total_interest,
        "loans": loans,
        "total_loan_principal": total_loan_principal,
        "total_loan_balance": total_loan_balance,
        "member_transactions": member_transactions,
        "recent_savings": recent_savings,
        "recent_loans": recent_loans,
        "net_position": net_position,
        "recent_ledger": recent_ledger,
        "loan_to_savings_ratio": loan_to_savings_ratio,
    }

    return render(request, "core/member_detail.html", context)




@login_required
def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Member updated successfully.")
            return redirect("member_detail", pk=member.pk)
    else:
        form = MemberForm(instance=member)
    return render(request, "core/member_form.html", {"form": form, "member": member})


@login_required
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        member.delete()
        messages.success(request, "🗑️ Member deleted.")
        return redirect("member_list")
    return render(request, "core/member_confirm_delete.html", {"member": member})
