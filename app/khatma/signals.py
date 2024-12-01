from django.db.models.signals import post_delete
from django.dispatch import receiver
from khatma.models import media,message

@receiver(post_delete, sender=media)
def delete_media_file(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)


@receiver(post_delete, sender=message)
def delete_related_media(sender,instance, **kwargs): # delete media instance after deleting the msg
    if instance.file:
        instance.file.delete()
        

