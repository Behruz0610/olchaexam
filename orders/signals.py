from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        print(f'Yangi order yaratildi: {instance}')
