from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@shared_task # NOTE: ONLY SYNC CODE IS ALLOWED HERE
def send_verification_email(): # TODO: SEND VERIFICATION EMAIL WHEN REGISTERING WITH EMAIL
    pass

