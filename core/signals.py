from django.db.models.signals import post_save
from django.dispatch import receiver

from ambassadors.models import MerchMiddle


@receiver(post_save, sender=MerchMiddle)
def created_ipr_notification(sender, instance: MerchMiddle, created, **kwargs):
    """Заполнение поля 'Архивная цена' при отправке мерча."""
    if created:
        instance.old_price = instance.merch.price
        instance.save()
