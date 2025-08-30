from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Account
from .forms import AccountForm

# List all accounts
def account_list(request):
    accounts = Account.objects.all().order_by("code")
    return render(request, "core/account_list.html", {"accounts": accounts})

# Create a new account
def account_create(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect("account_list")
    else:
        form = AccountForm()
    return render(request, "core/account_form.html", {"form": form})

# Edit an account
def account_edit(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated successfully.")
            return redirect("account_list")
    else:
        form = AccountForm(instance=account)
    return render(request, "core/account_form.html", {"form": form})
