import pytest
import requests
import json
from src import config
from src.data_store import channel_id_check
import time
from src.channel import channel_messages_v1

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

@pytest.fixture
def channel_priv(user1):
    c_priv = requests.post(config.url + 'channels/create/v2', json={
        "token": user1['token'],
        "name": "User1PrivChannel1",
        "is_public": False
        })
    return c_priv.json()

#test invalid token 

#test invalid channel id 

#test standup start while standup is already running 

#test user start standup but user is not in the channel 

def test_standup_start_basic(clear, user1, channel1):
    response1 = requests.post(config.url + 'standup/start/v1', json={
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 5
    })

    assert response1.status_code == 200 
    
    response = requests.get(config.url + 'standup/active/v1', params={
        'token': user1['token'],
        'channel_id': channel1['channel_id']
    })

    assert response.status_code == 200 
    assert response.json()['is_active'] == True

def test_standup_ends_basic(clear,user1, channel1):
    response1 = requests.post(config.url + 'standup/start/v1', json={
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 5
    })

    assert response1.status_code == 200 
    
    response = requests.get(config.url + 'standup/active/v1', params={
        'token': user1['token'],
        'channel_id': channel1['channel_id']
    })

    assert response.status_code == 200 
    assert response.json()['is_active'] == True
    time.sleep(5)
    
    response = requests.get(config.url + 'standup/active/v1', params={
        'token': user1['token'],
        'channel_id': channel1['channel_id']
    })

    assert response.status_code == 200 
    assert response.json()['is_active'] == False

def test_standup_send_basic(clear, user1, channel1):

    response1 = requests.post(config.url + 'standup/start/v1', json={
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 5
    })

    assert response1.status_code == 200 
    
    response = requests.get(config.url + 'standup/active/v1', params={
        'token': user1['token'],
        'channel_id': channel1['channel_id']
    })

    assert response.status_code == 200 
    assert response.json()['is_active'] == True

    response = requests.post(config.url + 'standup/send/v1', json={
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': "Bitcoin will hit 70k."
    })

    assert response.status_code == 200

    time.sleep(5)
    
    response = requests.get(config.url + 'standup/active/v1', params={
        'token': user1['token'],
        'channel_id': channel1['channel_id']
    })

    assert response.status_code == 200 
    assert response.json()['is_active'] == False

    

    

