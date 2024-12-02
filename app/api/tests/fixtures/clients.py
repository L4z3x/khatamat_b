import pytest
from api.models import MyUser
from rest_framework.test import APIClient,force_authenticate

@pytest.fixture
def get_or_create_user(db):
    user = MyUser.objects.filter(username="test").first()
    if not user:
        user = MyUser.objects.create_user(username="test",email="test@ex.com",password="weakpassword")
    return user
    
@pytest.fixture
def auth_api_client(get_or_create_user,db):
    user = get_or_create_user
    client = APIClient()
    res = client.post("/api/login/",
                {
                    "username":user.username,
                    "password": "weakpassword"
                })
    
    return res.data["access"], res.data["refresh"]


@pytest.fixture
def api_client(auth_api_client):
    access,refresh = auth_api_client
    client = APIClient()
    client.credentials(Authorization= f"Bearer {access}")
    return client


