import json
from django.shortcuts import render,HttpResponse
from channels.layers import get_channel_layer#You'll often want to send to the channel layer from outside of the scope of a consumer, and so you won't have self.channel_layer. In this case, you should use the get_channel_layer function to retrieve it:
from asgiref.sync import async_to_sync


# Create your views here.
def homeView(request):
    return render(request,'index.html',context={'room_name':'broadcast'})

def testView(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notificationbroadcast",
        {
            'type':'send_notification',
            'message': 'Notification'
        }
    )
    return HttpResponse("Done")

    ##By default the send(), group_send(), group_add() and other functions are async functions, meaning you have to await them. If you need to call them from synchronous code, you’ll need to use the handy asgiref.sync.async_to_sync wrapper:
