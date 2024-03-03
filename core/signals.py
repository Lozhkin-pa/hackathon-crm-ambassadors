from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify

from ambassadors.models import Ambassador, MerchMiddle
from content.models import Content

User = get_user_model()


@receiver(post_save, sender=MerchMiddle)
def filling_price_field(sender, instance: MerchMiddle, created, **kwargs):
    """Заполнение поля 'Архивная цена' при отправке мерча."""
    if created:
        instance.old_price = instance.merch.price
        instance.save()


@receiver(post_save, sender=Ambassador)
def new_ambassador_notification(
    sender, instance: Ambassador, created, **kwargs
):
    """Уведомления о новом Амбассадоре созданном через Яндекс Форму."""
    if created and instance.yandex_form:
        notify.send(
            sender=instance,
            # Получатель - заглушка, уведомления общие для всех.
            recipient=User.objects.last(),
            verb=f"Новый амбассадор: {instance.name}",
        )


@receiver(post_save, sender=Content)
def new_content_notification(sender, instance: Content, created, **kwargs):
    """Уведомления о новом контенте созданном через Яндекс Форму."""
    if created and instance.yandex_form:
        notify.send(
            sender=instance.ambassador,
            recipient=User.objects.last(),
            verb=f"{instance.ambassador.name} сделал(а) публикацию",
            description=instance.link,
        )
