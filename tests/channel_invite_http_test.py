import pytest
import requests
import json
from src import config

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
def channel1(user1):
    channel = requests.post(config.url + 'channels/create/v2', json={
        "token": user1['token'],
        "name": "FirstChannel",
        "is_public": True
        })
    return channel.json()

@pytest.fixture
def channel2(user1):
    c_priv = requests.post(config.url + 'channels/create/v2', json={
        "token": user1['token'],
        "name": "PrivChannel",
        "is_public": False
        })
    return c_priv.json()

@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1')


def test_channel_id_check(clear, channel1,user2, user1):
    resp = requests.post(config.url + 'channel/invite/v2', json={
        'token': user1['token'], 
        'channel_id': -1, 
        'u_id':user2['auth_user_id']
    })

    assert resp.status_code == 400

def test_token_check(clear, channel1,user2, user1):
    resp = requests.post(config.url + 'channel/invite/v2', json={
        'token': -1, 
        'channel_id': channel1['channel_id'], 
        'u_id':user2['auth_user_id']
    })

    assert resp.status_code == 403

def test_channel_implementation(clear, channel1,user2, user1):
    resp = requests.post(config.url + 'channel/invite/v2', json={
        'token': user1['token'], 
        'channel_id': channel1['channel_id'], 
        'u_id': user2['auth_user_id']
    })

    assert resp.status_code == 200

