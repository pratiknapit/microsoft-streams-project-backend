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
def channel_priv(user1):
    c_priv = requests.post(config.url + 'channels/create/v2', json={
        "token": user1['token'],
        "name": "PrivChannel",
        "is_public": False
        })
    return c_priv.json()

@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1')

def test_invalid_token(channel1):
    response = requests.post(config.url + 'channel/join/v2', json={
        "token": "randomtoken1",
        "channel_id": channel1['channel_id']
    })
    assert response.status_code == 403

def test_invalid_channel(user1):
    response = requests.post(config.url + 'channel/join/v2', json={
        "token": user1['token'],
        "channel_id": "randomchannel"
    })
    assert response.status_code == 400
    
def test_member_is_already_channel_members(clear, user1, channel1):
    response = requests.post(config.url + 'channel/join/v2', json={
        "token": user1['token'],
        "channel_id": channel1['channel_id']
    })
    assert response.status_code == 400
    

#This does not work for some reason, it is returning 400 error instead of 403.
def test_priv_channel_and_not_global_owner(clear, user1, user2, channel1, channel_priv):
    print(user1)
    print(user2)
    print(channel1)
    print(channel_priv)

    response = requests.post(config.url + 'channel/join/v2', json={
        "token": user2['token'],
        "channel_id": channel_priv['channel_id']
    })
    assert response.status_code == 403

def test_priv_channel_and_not_global_owner2():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + "auth/register/v2", json={
        "email": "pratik7@gmail.com",
        "password": "ronaldo",
        "name_first": "Pratik",
        "name_last": "Napit"
        })
    user1_payload = user1.json()

    user2 = requests.post(config.url + "auth/register/v2", json={
        "email": "afsadsf7@gmail.com",
        "password": "random123123",
        "name_first": "John",
        "name_last": "Dummmy"
        })
    user2_payload = user2.json()

    channel1 = requests.post(config.url + 'channels/create', json={
        "token": user1_payload['token'],
        "name": "FirstChannel",
        "is_public": True
        })
    channel1_payload = channel1.json()

    channel_priv = requests.post(config.url + 'channels/create/v2', json={
        "token": user1_payload['token'],
        "name": "PrivChannel",
        "is_public": False
        })
    priv_payload = channel_priv.json()

    print(user1_payload)
    print(user2_payload)
    print(channel1_payload)
    print(priv_payload)

    response = requests.post(config.url + 'channel/join/v2', json={
        "token": user2_payload['token'],
        "channel_id": priv_payload['channel_id']
    })
    assert response.status_code == 403


def test_basic_func_channel_details_v2():
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + "auth/register/v2", json={
        "email": "pratik7@gmail.com",
        "password": "ronaldo",
        "name_first": "Pratik",
        "name_last": "Napit"
        })
    user1_payload = response.json()
    assert response.status_code == 200

    response2 = requests.post(config.url + "auth/register/v2", json={
        "email": "dummy7@gmail.com",
        "password": "yessir",
        "name_first": "Liam",
        "name_last": "Maverick"
        })
    user2_payload = response2.json()
    assert response2.status_code == 200

    response_c = requests.post(config.url + 'channels/create/v2', json={
        "token": user1_payload['token'],
        "name": "FirstChannel",
        "is_public": "True"
        })
    
    channel_payload = response_c.json()
    assert response_c.status_code == 200

    response_j = requests.post(config.url + 'channel/join/v2', json={
        "token": user2_payload['token'],
        "channel_id": channel_payload['channel_id']
    })
    assert response_j.status_code == 200