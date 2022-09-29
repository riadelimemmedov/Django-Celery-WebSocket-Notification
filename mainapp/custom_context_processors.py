from notifications_app.models import BroadcastNotification

#!all_broadcast_notifications
def all_broadcast_notifications(request):
    notifications = BroadcastNotification.objects.filter(send=True)
    print('All notifications come from database ', notifications)
    return {'notifications':notifications,'notification_count':notifications.count()}