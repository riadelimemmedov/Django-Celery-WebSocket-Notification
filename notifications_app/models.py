from email.policy import default
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_celery_beat.models import MINUTES,PeriodicTask, CrontabSchedule, PeriodicTasks
import json

# Create your models here.

#!BroadcastNotification
class BroadcastNotification(models.Model):
    message = models.TextField()
    send = models.BooleanField(default=False)
    broadcast_on = models.DateTimeField()
    
    def __str__(self):
        return str(self.send)
    
    class Meta:
        ordering = ['-broadcast_on']
        verbose_name = 'BroadcastNotification'
        verbose_name_plural = 'BroadcastNotifications'
#?Create BroadcastNotification With Django Signals
@receiver(post_save,sender=BroadcastNotification)
def notification_handler(sender,instance,created,**kwargs):
    # call group_send function directly to send notificatoions or you can create a dynamic task in celery beat
    if created:
        schedule, created = CrontabSchedule.objects.get_or_create(hour = instance.broadcast_on.hour, minute = instance.broadcast_on.minute, day_of_month = instance.broadcast_on.day, month_of_year = instance.broadcast_on.month)
        task = PeriodicTask.objects.create(crontab=schedule, name="broadcast-notification-"+str(instance.id), task="broadcast_notification", args=json.dumps((instance.id,)))#if encounter task name used this method => notifications_app.tasks.broadcast_notification
        print('Task ', task)
    #else or if not created:
        #pass