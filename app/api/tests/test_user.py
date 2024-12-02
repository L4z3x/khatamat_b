import pytest

def test_unAuth_req(api_client):
    res = api_client.get('/api/update')
    assert res.status_code == 301

def test_create_account(api_client,db): # test creating a account
    res = api_client.post("/api/signup/",{
        "username":"test",
        "email":"test@ex.com",
        "password":"weakpassword"
    })
    assert res.status_code == 201
    
def test_create_account_malformed(api_client,db):
    res = api_client.post("/api/signup/",{
        "username":"test_user",
        "email":"test@ex.com",
    })
    assert res.status_code == 400
    
def test_user_account(api_client,db):
    res = api_client.get("/api/account/",
                    headers={'Authorization': api_client._credentials['Authorization']})
    assert res.status_code == 200
    assert res.data['username'] == "test"
    assert res.data['email'] == "test@ex.com"
    
def test_update_user_account(api_client,db):
    access_token = api_client._credentials['Authorization']
    res = api_client.post("/api/update/",{
        "gender":"male"
        },headers={
            'Authorization': access_token
            })
    assert res.status_code == 202 
    
def test_delete_user_account(get_or_create_user,api_client,db):
    user = get_or_create_user
    # breakpoint()
    res = api_client.delete(f"/api/delete/{user.id}/",
                    headers={'Authorization': api_client._credentials['Authorization']})
    assert res.status_code == 204

