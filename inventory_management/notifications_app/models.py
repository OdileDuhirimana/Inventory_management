from django.db import models
from django.conf import settings
from notifications.models import Notification as BaseNotification
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Notification(BaseNotification):
    recipient_user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-timestamp']
