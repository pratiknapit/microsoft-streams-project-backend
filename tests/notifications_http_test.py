import pytest
import requests
import json
from src import config
from src import data_store


@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1')

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

@pytest.fixture
def user3():
    email = "testmail3@gamil.com"
    password = "Testpass1"
    first_name = "three"
    last_name = "lastname"
    user3 = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    })
    return user3.json() 

@pytest.fixture
def channel1(user1):
    channel = requests.post(config.url + 'channels/create/v2', json={
        "token": user1['token'],
        "name": "User1Channel1",
        "is_public": True
        })
    return channel.json()

@pytest.fixture
def channel2(user2):
    channel = requests.post(config.url + 'channels/create/v2', json={
        "token": user2['token'],
        "name": "User2Channel1",
        "is_public": True
        })
    return channel.json()


def test_notifications_returns_correctly(clear, user1, user2, channel1):

    response = requests.post(config.url + 'channel/join/v2', json={
        "token": user2['token'],
        "channel_id": 1
    })

    assert response.status_code == 200

    message_og = requests.post(config.url + 'message/send/v1', json= {
        'token': user1['token'],
        'channel_id': 1,
        'message': 'Crypto will bounce after this dip.'
    })

    assert message_og.status_code == 200

    msg_og = message_og.json() 

    response = requests.post(config.url + 'message/react/v1', json= {
        'token': user2['token'],
        'message_id': msg_og['message_id'],
        'react_id': 1 
    })

    assert response.status_code == 200

    resp = requests.get(config.url + 'notifications/get/v1', params={
        'token': user1['token']
    })

    assert resp.status_code == 200

    resp = requests.get(config.url + 'notifications/get/v1', params={
        'token': user2['token']
    })

    assert resp.status_code == 200

def test_notifications_structure(clear, user1, user2, channel1):
    response = requests.post(config.url + 'channel/join/v2', json={
        "token": user2['token'],
        "channel_id": 1
    })

    assert response.status_code == 200

    message_og = requests.post(config.url + 'message/send/v1', json= {
        'token': user1['token'],
        'channel_id': 1,
        'message': 'Crypto will bounce after this dip.'
    })

    assert message_og.status_code == 200

    msg_og = message_og.json() 

    response = requests.post(config.url + 'message/react/v1', json= {
        'token': user2['token'],
        'message_id': msg_og['message_id'],
        'react_id': 1 
    })

    assert response.status_code == 200

    resp = requests.get(config.url + 'notifications/get/v1', params={
        'token': user1['token']
    })

    assert resp.status_code == 200

    