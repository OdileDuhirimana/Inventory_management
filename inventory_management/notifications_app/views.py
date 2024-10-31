from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from notifications.models import Notification

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'notifications.html', {'notifications': notifications})
