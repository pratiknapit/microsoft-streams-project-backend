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

def test_invalid_token(clear, user1, channel1):
    response = requests.get(config.url + 'channel/details/v2', params = {
        'token': "random_token",
        'channel_id': channel1["channel_id"]
    })

    assert response.status_code == 403

def test_invalid_channel(clear, user1):
    response = requests.get(config.url + 'channel/details/v2', params = {
        'token': user1['token'],
        'channel_id': "random_channel_id"
    })
    assert response.status_code == 400

def test_user_is_not_member_of_channel(clear, user2, channel1):
    response = requests.get(config.url + 'channel/details/v2', params = {
        'token': user2['token'],
        'channel_id': channel1["channel_id"]
    })
    assert response.status_code == 403
    

def test_channel_details_v2():
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + "auth/register/v2", json={
        "email": "pratik7@gmail.com",
        "password": "ronaldo",
        "name_first": "Pratik",
        "name_last": "Napit"
        })
    user_payload = response.json()
    assert response.status_code == 200

    response_c = requests.post(config.url + 'channels/create/v2', json={
        "token": user_payload['token'],
        "name": "FirstChannel",
        "is_public": "True"
        })
    
    channel_payload = response_c.json()
    assert response_c.status_code == 200

    response_det = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_payload['token'],
        'channel_id': channel_payload["channel_id"]
    })

    detail_payload = response_det.json()
    assert response_det.status_code == 200

    assert detail_payload == {
        'name': "FirstChannel",
        'is_public': 'True',
        'owner_members':[{
            'u_id':user_payload['auth_user_id'], 
            "email":"pratik7@gmail.com", 
            'name_first':"Pratik",
            'name_last':"Napit",
            'handle_str':"pratiknapit",
        }],
        'all_members':[{
            'u_id':user_payload['auth_user_id'], 
            "email":"pratik7@gmail.com", 
            'name_first':"Pratik",
            'name_last':"Napit",
            'handle_str':"pratiknapit",
        }]               
        
    }
