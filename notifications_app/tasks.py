from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import asyncio
import json

from celery import Celery,states
from celery.exceptions import Ignore

from .models import BroadcastNotification

@shared_task(bind=True,name='broadcast_notification')
def broadcast_notification(self,data):
    print('Data celery', data)
    try:
        notification = BroadcastNotification.objects.filter(id=int(data))
        if len(notification)>0:
            print('noldu amk notification ', notification )
            notification = notification.first()
            channel_layer = get_channel_layer()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(channel_layer.group_send(
                "notificationbroadcast",
                {
                    'type':'send_notification',
                    'message': json.dumps(notification.message)
                }
            ))
            notification.send = True
            notification.save()
            return 'Done'
        else:
            self.update_state(
                state='FAILURE',
                meta = {'exe':'Not Found Broadcast'}
            )
            raise Ignore()
    except:
        self.update_state(
            state = 'FAILURE',
            meta = {
                'exe':'Failed Running'
                # 'exc_type': type(ex).__name__,
                # 'exc_message': traceback.format_exc().split('\n')
                # 'custom': '...'
            }
        )
        
        raise Ignore()
