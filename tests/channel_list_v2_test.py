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
def channel1(user1):
    channel = requests.post(config.url + 'channels/create/v2', json={
        "token": user1['token'],
        "name": "FirstChannel",
        "is_public": True
        })
    return channel.json()

def test_invalid_token_list():
    requests.delete(config.url + 'clear/v1')
    response = requests.get(config.url + 'channels/list/v2', params = {
        'token': "random_token"
    })
    assert response.status_code == 403

def test_invalid_token_listall():
    requests.delete(config.url + 'clear/v1')
    response = requests.get(config.url + 'channels/listall/v2', params = {
        'token': "random_token"
    })
    assert response.status_code == 403

def test_valid_token_list(user1):
    requests.delete(config.url + 'clear/v1')
    response = requests.get(config.url + 'channels/list/v2', params = {
        'token': user1['token']
    })
    assert response.status_code == 200

def test_valid_token_listall(user1):
    requests.delete(config.url + 'clear/v1')
    response = requests.get(config.url + 'channels/listall/v2', params = {
        'token': user1['token']
    })
    assert response.status_code == 200

def test_channel_list_listall_v2_basic(): 
    requests.delete(config.url + 'clear/v1')
    response_j = requests.post(config.url + "auth/register/v2", json={
    "email": "use4r@gmail.com",
    "password": "dummypass",
    "name_first": "jacky",
    "name_last": "zhu"
    })

    response_p = requests.post(config.url + "auth/register/v2", json={
    "email": "pratik7@gmail.com",
    "password": "ronaldo",
    "name_first": "Pratik",
    "name_last": "Napit"
    })

    user_j_payload = response_j.json()
    user_p_payload = response_p.json()
    assert response_j.status_code == 200
    assert response_p.status_code == 200

    response1 = requests.post(config.url + 'channels/create/v2', json={
        "token": user_j_payload['token'],
        "name": "FirstChannel",
        "is_public": "True"
        })
    
    response_cp = requests.post(config.url + 'channels/create/v2', json={
        "token": user_p_payload['token'],
        "name": "IshaChannel",
        "is_public": "True"
        })

    channel_payload = response1.json()
    assert response1.status_code == 200
    assert response_cp.status_code == 200
    assert channel_payload == {"channel_id": 1}


    response2 = requests.get(config.url + 'channels/list/v2', params = {
        'token': user_j_payload['token']
    })

    list_payload = response2.json()['channels']
    assert list_payload == [{
        "channel_id": 1,
        "name": "FirstChannel"
    }]

    #testing list all route 
    response3 = requests.get(config.url + 'channels/listall/v2', params = {
        'token': user_j_payload['token']
    })
    listall_payload = response3.json()['channels']
    assert listall_payload == [{
        "channel_id": 1,
        "name": "FirstChannel"
    },{
        "channel_id": 2,
        "name": "IshaChannel"
    }]

