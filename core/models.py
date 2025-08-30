# core/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class AccountType(models.TextChoices):
    ASSET = "ASSET", "Asset"
    LIABILITY = "LIABILITY", "Liability"
    EQUITY = "EQUITY", "Equity"
    INCOME = "INCOME", "Income"
    EXPENSE = "EXPENSE", "Expense"

class ReportTag(models.TextChoices):
    # Income statement tags
    INCOME_INTEREST_ON_LOANS = "INCOME_INTEREST_ON_LOANS", "Interest from loans"
    INCOME_DONATION = "INCOME_DONATION", "Donation income"
    INCOME_LAP_FORMS = "INCOME_LAP_FORMS", "Income from LAP forms"
    INCOME_REGISTRATION_FEES = "INCOME_REGISTRATION_FEES", "Registration fee income"
    EXP_BANK_CHARGES = "EXP_BANK_CHARGES", "Bank charges"
    EXP_MEETING = "EXP_MEETING", "Meeting expenses"
    EXP_ACCOUNTANCY = "EXP_ACCOUNTANCY", "Accountancy fees"
    EXP_AGM = "EXP_AGM", "AGM expenses"
    EXP_BAD_DEBT_PROVISION = "EXP_BAD_DEBT_PROVISION", "Provision for bad debts"
    EXP_HONORARIA = "EXP_HONORARIA", "Honoraria"
    EXP_AUDIT_FEES = "EXP_AUDIT_FEES", "Audit fees"

    # Balance sheet tags
    ASSET_CASH_EQUITY = "ASSET_CASH_EQUITY", "Cash at bank - Equity"
    ASSET_LOANS_PRINCIPAL = "ASSET_LOANS_PRINCIPAL", "Loans receivable - principal"
    ASSET_LOAN_INTEREST = "ASSET_LOAN_INTEREST", "Interest receivable on loans"
    ASSET_RECEIVABLE_HIGHLANDS = "ASSET_RECEIVABLE_HIGHLANDS", "Receivable from Highlands Ltd"
    LIAB_MEMBERS_SAVINGS = "LIAB_MEMBERS_SAVINGS", "Total members savings"
    LIAB_ACCOUNTS_PAYABLE = "LIAB_ACCOUNTS_PAYABLE", "Accounts payable"
    EQUITY_SHARE_CAPITAL = "EQUITY_SHARE_CAPITAL", "Share capital"
    EQUITY_RETAINED_EARNINGS = "EQUITY_RETAINED_EARNINGS", "Retained earnings"
    EQUITY_CURRENT_YEAR_SURPLUS = "EQUITY_CURRENT_YEAR_SURPLUS", "Surplus for the year"

class Account(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=20, choices=AccountType.choices)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT)
    report_tag = models.CharField(max_length=64, choices=ReportTag.choices, null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class JournalEntry(models.Model):
    date = models.DateField()
    memo = models.CharField(max_length=255, blank=True)
    reference = models.CharField(max_length=50, blank=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    posted = models.BooleanField(default=True)  # allow draft entries if needed
    created_at = models.DateTimeField(auto_now_add=True)

class JournalLine(models.Model):
    entry = models.ForeignKey(JournalEntry, related_name="lines", on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    debit = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        indexes = [
            models.Index(fields=["account"]),
            models.Index(fields=["entry", "account"]),
        ]

# members/models.py
class Member(models.Model):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    STATUS_CHOICES = [(ACTIVE, "Active"), (INACTIVE, "Inactive")]

    member_no = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=120)
    id_number = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    joined_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.member_no} - {self.full_name}"

