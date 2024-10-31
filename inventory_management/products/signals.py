from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib import messages
from .models import Product

@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    if instance.low_stock_alert:  
        messages.warning(request, f'Low stock alert for: {instance.name}')

@receiver(post_delete, sender=Product)
def product_deleted(sender, instance, **kwargs):
    messages.warning(request, f'Product deleted: {instance.name}')
