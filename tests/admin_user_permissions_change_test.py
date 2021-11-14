import pytest
import requests
import json
from src import config

OWNER_PERMISSION = 1
MEMBER_PERMISSION = 2 

@pytest.fixture(autouse=True)
def clear():
    requests.delete(config.url + '/clear/v1')
    yield
    requests.delete(config.url + '/clear/v1')


@pytest.fixture
def user1(clear):
    email = "testmail@gamil.com"
    password = "Testpass12345"
    first_name = "firstone"
    last_name = "lastone"
    user1 = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    })

    return user1.json()

@pytest.fixture
def user2():
    email = "testmail2@gamil.com"
    password = "Testpass123456"
    first_name = "firsttwo"
    last_name = "lasttwo"
    user2 = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    })
    return user2.json() 

def test_invalid_token(clear, user1, user2):
    response = requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': 1238782,
        'u_id': user2['auth_user_id'],
        'permission_id': OWNER_PERMISSION
    })

    assert response.status_code == 403


def test_invalid_user(clear, user1, user2):
    response = requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': user1['token'],
        'u_id': 67,
        'permission_id': OWNER_PERMISSION
    })

    assert response.status_code == 400

def test_invalid_permission(clear, user1, user2):
    response = requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': user1['token'],
        'u_id': user2['auth_user_id'],
        'permission_id': 4
    })

    assert response.status_code == 400

def test_permissions_change_basic(clear, user1, user2):
    response = requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': user1['token'],
        'u_id': user2['auth_user_id'],
        'permission_id': OWNER_PERMISSION
    })

    assert response.status_code == 200

def test_permissions_change_by_member(clear, user1, user2):

    response = requests.post(config.url + 'admin/userpermission/change/v1', json={
        'token': user2['token'],
        'u_id': user1['auth_user_id'],
        'permission_id': MEMBER_PERMISSION
    })

    assert response.status_code == 403
