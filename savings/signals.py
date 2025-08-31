# savings/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SavingsTransaction
from core.models import MemberTransaction  # adjust path as needed

@receiver(post_save, sender=SavingsTransaction)
def sync_member_transaction(sender, instance, created, **kwargs):
    member = instance.savings_account.member
    source_model = 'SavingsTransaction'
    source_id = instance.id

    defaults = {
        'member': member,
        'date': instance.date,
        'amount': instance.amount,
        'description': instance.notes or f"{instance.transaction_type} via Savings",
        'transaction_type': f"Savings {instance.transaction_type.title()}",
        'journal_entry': instance.journal_entry,
    }

    MemberTransaction.objects.update_or_create(
        source_model=source_model,
        source_id=source_id,
        defaults=defaults
    )
