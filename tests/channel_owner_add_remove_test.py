import pytest
import requests
import json
from src import config

@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1')

@pytest.fixture
def user1(clear):
    user1 = requests.post(config.url + "auth/register/v2", json={
        "email": "pratik7@gmail.com",
        "password": "ronaldo",
        "name_first": "Pratik",
        "name_last": "Napit"
        })
    return user1.json()

@pytest.fixture
def user2():
    user2 = requests.post(config.url + "auth/register/v2", json={
        "email": "afsadsf7@gmail.com",
        "password": "random123123",
        "name_first": "John",
        "name_last": "Dummmy"
        })
    return user2.json()

@pytest.fixture
def user3():
    user3 = requests.post(config.url + "auth/register/v2", json={
        "email": "computernerd45@gmail.com",
        "password": "bestgate",
        "name_first": "RandomGuy",
        "name_last": "Yummy"
        })
    return user3.json()

@pytest.fixture
def channel1(user1):
    channel = requests.post(config.url + 'channels/create/v2', json={
        "token": user1['token'],
        "name": "FirstChannel",
        "is_public": True
        })
    return channel.json()

def test_invalid_token_add(clear, user1, channel1, user2):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/addowner/v1', json={
        "token": "random_token",
        "channel_id": channel1['channel_id'],
        "u_id": user2['auth_user_id']
    })
    assert response.status_code == 403

def test_invalid_token_remove(clear, user1, channel1, user2):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/addowner/v1', json={
        "token": "random_token",
        "channel_id": channel1['channel_id'],
        "u_id": user2['auth_user_id']
    })
    assert response.status_code == 403

def test_invalid_channel_add(clear, user1, channel1, user2):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/addowner/v1', json={
        "token": user1['token'],
        "channel_id": "random_channel_id",
        "u_id": user2['auth_user_id']
    })
    assert response.status_code == 400

def test_invalid_channel_remove(user1, channel1, user2):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/removeowner/v1', json={
        "token": user1['token'],
        "channel_id": "random_channel_id",
        "u_id": user2['auth_user_id']
    })
    assert response.status_code == 400

def test_invalid_user_add(clear, user1, channel1, user2):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/addowner/v1', json={
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "u_id": "random_user"
    })
    assert response.status_code == 400

def test_invalid_user_remove(clear, user1, channel1, user2):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/removeowner/v1', json={
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "u_id": "random_user"
    })
    assert response.status_code == 400

def test_user_is_not_channel_member_add(clear, user1, channel1, user2, user3):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/addowner/v1', json={
        "token": user3['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user2['auth_user_id']
    })
    assert response.status_code == 400

def test_user_is_not_channel_member_remove(clear, user1, channel1, user2, user3):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/removeowner/v1', json={
        "token": user3['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user2['auth_user_id']
    })
    assert response.status_code == 400

def test_user_is_already_channel_owner_add(clear, user1, channel1, user2, user3):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/addowner/v1', json={
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user1['auth_user_id']
    })
    assert response.status_code == 400

def test_user_is_already_channel_owner_remove(clear, user1, channel1, user2, user3):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/removeowner/v1', json={
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user1['auth_user_id']
    })
    assert response.status_code == 400

def test_no_owner_permission_add(clear, user1, channel1, user2, user3):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/addowner/v1', json={
        "token": user2['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user3['auth_user_id']
    })
    assert response.status_code == 403

def test_no_owner_permission_add(clear, user1, channel1, user2, user3):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/removeowner/v1', json={
        "token": user2['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user3['auth_user_id']
    })
    
    assert response.status_code == 400

def test_channel_add_remove_owner1(clear, user1, user2, channel1):
    r1 = requests.post(config.url + 'channel/join/v2', json={
        "token": user2['token'],
        "channel_id": channel1['channel_id']
    })
    assert r1.status_code == 200

    r2 = requests.post(config.url + 'channel/addowner/v1', json={
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user2['auth_user_id']
    })
    assert r2.status_code == 200

    r3 = requests.post(config.url + 'channel/removeowner/v1', json={
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user2['auth_user_id']
    })
    assert r3.status_code == 200

