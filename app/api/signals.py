from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MyUser

@receiver(post_save, sender=MyUser)
def update_brothers_num(sender, instance, **kwargs):
    if kwargs.get('created', False):
        return  # Skip if the user is being created
    instance.brothersNum = len(set(instance.brothers.all() | instance.brothers_set.all()))
    instance.save(update_fields=['brothersNum'])