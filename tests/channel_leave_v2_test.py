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
def channel1(user1):
    channel = requests.post(config.url + 'channels/create/v2', json={
        "token": user1['token'],
        "name": "FirstChannel",
        "is_public": True
        })
    return channel.json()

def test_invalid_token(clear, channel1):
    response = requests.post(config.url + 'channel/leave/v1', json={
        "token": "random_token",
        "channel_id": channel1['channel_id']
        })
    assert response.status_code == 403

def test_invalid_channel_id(clear, user1):
    response = requests.post(config.url + 'channel/leave/v1', json={
        "token": user1['token'],
        "channel_id": "random_channel_id"
        })
    assert response.status_code == 400

def test_user_is_not_channel_member(user2, channel1):
    response = requests.post(config.url + 'channel/leave/v1', json={
        "token": user2['token'],
        "channel_id": channel1['channel_id']
        })
    assert response.status_code == 403

def test_channel_leave_v2_functionality():
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
    assert response2.status_code == 200

    response3 = requests.post(config.url + 'channels/create/v2', json={
        "token": user1_payload['token'],
        "name": "FirstChannel",
        "is_public": "True"
        })
    channel_payload = response3.json()
    assert response3.status_code == 200

    response5 = requests.post(config.url + 'channel/leave/v1', json={
        "token": user1_payload['token'],
        "channel_id": channel_payload['channel_id']
        })
    leave_payload = response5.json()
    assert response5.status_code == 200
    assert leave_payload == {}
    
    response_det = requests.get(config.url + 'channel/details/v2', params = {
        'token': user1_payload['token'],
        'channel_id': channel_payload["channel_id"]
    })
    assert response_det.status_code == 403


