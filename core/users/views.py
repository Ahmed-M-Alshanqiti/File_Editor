# users/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from files.models import Notification

def user_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'users/user_list.html', {'users': users})

def profile_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/profile_detail.html', {'profile_user': user})


@login_required
def notifications_list(request):
    notifications = request.user.notifications.select_related('sender', 'related_file')
    if request.method == 'POST':
        request.user.notifications.filter(is_read=False).update(is_read=True)
        return redirect('notifications')
    return render(request, 'users/notifications.html', {'notifications': notifications})


@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')
