from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Account, JournalEntry
from .forms import AccountForm, JournalEntryForm, JournalLineFormSet


# -----------------------------
# ACCOUNT VIEWS
# -----------------------------

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
            # Ignore deleted rows when summing
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
        form = JournalEntryForm()
        formset = JournalLineFormSet()

    return render(request, "core/journal_entry_form.html", {"form": form, "formset": formset})


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
        form = JournalEntryForm(instance=entry)
        formset = JournalLineFormSet(instance=entry)

    return render(request, "core/journal_entry_form.html", {"form": form, "formset": formset})


@login_required
def journal_entry_delete(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk)
    if request.method == "POST":
        entry.delete()
        messages.success(request, "🗑️ Journal entry deleted.")
        return redirect("journal_entry_list")
    return render(request, "core/journal_entry_confirm_delete.html", {"entry": entry})
