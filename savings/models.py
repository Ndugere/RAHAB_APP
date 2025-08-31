from django.db import models
from django.utils import timezone
from core.models import Account, JournalEntry, Member

class SavingsAccount(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)  # Should have ReportTag.LIAB_MEMBERS_SAVINGS
    opened_on = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Savings - {self.member.full_name}"

    @property
    def balance(self):
        total_deposits = self.transactions.filter(transaction_type='DEPOSIT').aggregate(models.Sum('amount'))['amount__sum'] or 0
        total_withdrawals = self.transactions.filter(transaction_type='WITHDRAWAL').aggregate(models.Sum('amount'))['amount__sum'] or 0
        total_interest = self.transactions.filter(transaction_type='INTEREST').aggregate(models.Sum('amount'))['amount__sum'] or 0
        return total_deposits + total_interest - total_withdrawals

    def deposit(self, amount, note=""):
        from savings.models import SavingsTransaction  # Avoid circular import
        SavingsTransaction.objects.create(
            savings_account=self,
            transaction_type='DEPOSIT',
            amount=amount,
            notes=note
        )

    def withdraw(self, amount, note=""):
        from savings.models import SavingsTransaction
        SavingsTransaction.objects.create(
            savings_account=self,
            transaction_type='WITHDRAWAL',
            amount=amount,
            notes=note
        )

class SavingsTransaction(models.Model):
    DEPOSIT = 'DEPOSIT'
    WITHDRAWAL = 'WITHDRAWAL'
    INTEREST = 'INTEREST'
    TRANSACTION_TYPES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
        (INTEREST, 'Interest Credit'),
    ]

    savings_account = models.ForeignKey(SavingsAccount, related_name='transactions', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    journal_entry = models.ForeignKey(JournalEntry, null=True, blank=True, on_delete=models.SET_NULL)
    notes = models.CharField(max_length=255, blank=True)
    source = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional tag for transaction origin (e.g. 'Loan Overpayment', 'Mobile Deposit', 'Manual Entry')"
    )

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} on {self.date} ({self.savings_account.member.full_name})"
