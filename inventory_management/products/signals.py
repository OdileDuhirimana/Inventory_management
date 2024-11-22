from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from notifications.signals import notify
from django.contrib import messages
from .models import Product

@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    if created:
        messages.success(request, f'Product created: {instance.name}')
        
        if instance.low_stock_alert:  
            notify.send(
                actor=instance,
                recipient=instance.owner,  
                verb='Low stock alert',
                action_object=instance,
                description=f'Low stock alert for: {instance.name}'
            )
    else:
        
        messages.info(request, f'Product updated: {instance.name}')

       
        if instance.low_stock_alert:  
            notify.send(
                actor=instance,
                recipient=instance.owner,
                verb='Low stock alert',
                action_object=instance,
                description=f'Low stock alert for: {instance.name}'
            )

@receiver(post_delete, sender=Product)
def product_deleted(sender, instance, **kwargs):
    messages.warning(request, f'Product deleted: {instance.name}')
