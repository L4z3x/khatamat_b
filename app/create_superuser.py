import os

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

MyUser = get_user_model()

ADMIN_ACCOUNT = os.environ.get('ADMIN_ACCOUNT', 'admin@khatamat.test')
ADMIN_ACCOUNT_PASSWORD = os.environ.get(
    'ADMIN_ACCOUNT_PASSWORD', 'admin')


def create_admins(MyUser, username, email, password):
    """
    create superuser
    """
    try:
        MyUser.objects.get(email=email)
        print("User "+username+" already exist <----- ", flush=True)
    except MyUser.DoesNotExist:
        u = MyUser.objects.create_superuser(
            username, email, password, fullname="admin")
        print("User "+username+" created with default password'")


create_admins(MyUser, "admin", ADMIN_ACCOUNT, ADMIN_ACCOUNT_PASSWORD)
