from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import MyUser,UserSetting

@receiver(post_save, sender=MyUser)
def update_brothers_num(sender, instance, **kwargs):
    if kwargs.get('created', False) and not hasattr(instance, 'setting'):
        # create user setting
        UserSetting.objects.create(user=instance)
        return 
    
    # Avoid recursion by using a flag
    if getattr(instance, '_updating_brothers_num', False):
        return

    # Set the flag to avoid recursion
    instance._updating_brothers_num = True
    try:
        instance.setting.brothersNum = len(set(instance.brothers.all() | instance.brothers_set.all()))
        instance.setting.save(update_fields=['brothersNum'])
    finally:
        # Ensure the flag is reset
        instance._updating_brothers_num = False


@receiver(post_delete, sender=MyUser)
def delete_user_setting(sender, instance, **kwargs):
    if hasattr(instance, 'setting'):
        instance.setting.delete()
        return