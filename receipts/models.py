import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from core.models import Member, JournalEntry

User = get_user_model()

class Receipt(models.Model):
    LOAN = "LOAN"
    SAVINGS = "SAVINGS"
    TYPE_CHOICES = [(LOAN, "Loan Repayment"), (SAVINGS, "Savings Deposit")]

    receipt_no = models.CharField(max_length=36, unique=True, editable=False)  # UUID-based
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    issued_on = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=50, blank=True)  # e.g. Cash, Mobile, Bank
    reference_note = models.TextField(blank=True)

    # Source links
    loan_repayment = models.OneToOneField(
        'loans.LoanRepayment', null=True, blank=True, on_delete=models.SET_NULL
    )
    savings_transaction = models.OneToOneField(
        'savings.SavingsTransaction', null=True, blank=True, on_delete=models.SET_NULL
    )

    journal_entry = models.ForeignKey(JournalEntry, null=True, blank=True, on_delete=models.SET_NULL)

    # Audit trail
    issued_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Receipt #{self.receipt_no} - {self.member.full_name}"

    def save(self, *args, **kwargs):
        if not self.receipt_no:
            self.receipt_no = str(uuid.uuid4())  # Auto-generate UUID
        super().save(*args, **kwargs)
