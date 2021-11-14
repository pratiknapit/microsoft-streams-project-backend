import pytest
import requests
import json
from src import config

@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1')

@pytest.fixture
def user1():
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

#invalid token 

def test_invalid_token_r(clear, user1, channel1):
    msg = requests.post(config.url + 'message/send/v1', json= {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': 'Crypto will bounce after this dip.'
    })

    assert msg.status_code == 200

    mog = msg.json()['message_id'] 
 
    response = requests.post(config.url + 'message/react/v1', json= {
        'token': 123123,
        'message_id': mog,
        'react_id': 1 
    })

    assert response.status_code == 403

def test_invalid_token_unreact(clear, user1, channel1):
    msg = requests.post(config.url + 'message/send/v1', json= {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': 'Crypto will bounce after this dip.'
    })

    assert msg.status_code == 200

    mog = msg.json()['message_id'] 

    status_code = requests.post(config.url + 'message/unreact/v1', json={
        'token': "invalid_token",
        'message_id': mog,
        'react_id': 1
    }).status_code

    assert status_code == 403

def test_invalid_react_id1(clear, user1, channel1):
    msg = requests.post(config.url + 'message/send/v1', json= {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': 'Crypto will bounce after this dip.'
    })

    assert msg.status_code == 200

    mog = msg.json()['message_id']

    channel = requests.post(config.url + 'message/react/v1', json={
        'token': user1['token'],
        'message_id': mog,
        'react_id': 0
    })

    assert channel.status_code == 400

def test_invalid_react_id(clear, user1, channel1):
    msg = requests.post(config.url + 'message/send/v1', json= {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': 'Crypto will bounce after this dip.'
    })

    assert msg.status_code == 200

    mog = msg.json()['message_id'] 
    channel_status_code = requests.post(config.url + 'message/unreact/v1', json={
        'token': user1['token'],
        'message_id': mog,
        'react_id': 0
    }).status_code

    assert channel_status_code == 400

#Channel does not exist
def test_reaction_channel_react(clear, user1, channel1):
    msg = requests.post(config.url + 'message/send/v1', json= {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': 'Crypto will bounce after this dip.'
    })

    assert msg.status_code == 200

    mog = msg.json()['message_id'] 

    channel_status_code = requests.post(config.url + 'message/unreact/v1',
                                        json={'token': user1['token'], 'message_id': mog, 'react_id': 1}).status_code

    assert channel_status_code == 200

def test_reaction_channel_unreact(clear, user1, channel1):
    msg = requests.post(config.url + 'message/send/v1', json= {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': 'Crypto will bounce after this dip.'
    })

    assert msg.status_code == 200

    mog = msg.json()['message_id'] 

    channel_status_code = requests.post(config.url + 'message/react/v1',
                                        json={'token': user1['token'], 'message_id': mog, 'react_id': 1}).status_code

    assert channel_status_code == 200

#1000 characters 

#pair of channel and dm_id are valid and the auth user has not
#joined the channel or dm they are trying to share the message to

def test_message_react_to_channel_msg(clear, user1, user2, channel1):
    response = requests.post(config.url + 'channel/join/v2', json={
        "token": user2['token'],
        "channel_id": 1
    })

    assert response.status_code == 200

    msg = requests.post(config.url + 'message/send/v1', json= {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': 'Crypto will bounce after this dip.'
    })

    assert msg.status_code == 200

    mog = msg.json()['message_id']  

    response = requests.post(config.url + 'message/react/v1', json= {
        'token': user2['token'],
        'message_id': mog,
        'react_id': 1 
    })

    assert response.status_code == 200

def test_message_react_by_ownself(clear, user1, user2, channel1, channel2):
    response = requests.post(config.url + 'channel/join/v2', json={
        "token": user2['token'],
        "channel_id": 1
    })

    assert response.status_code == 200

    msg = requests.post(config.url + 'message/send/v1', json= {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': 'Crypto will bounce after this dip.'
    })

    assert msg.status_code == 200

    mog = msg.json()['message_id']  

    response = requests.post(config.url + 'message/react/v1', json= {
        'token': user1['token'],
        'message_id': mog,
        'react_id': 1 
    })

    assert response.status_code == 200 

def test_message_unreact(clear, user1, user2, channel1, channel2):
    response = requests.post(config.url + 'channel/join/v2', json={
        "token": user2['token'],
        "channel_id": 1
    })

    assert response.status_code == 200

    msg = requests.post(config.url + 'message/send/v1', json= {
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'message': 'Crypto will bounce after this dip.'
    })

    assert msg.status_code == 200

    mog = msg.json()['message_id'] 

    response = requests.post(config.url + 'message/react/v1', json= {
        'token': user2['token'],
        'message_id': mog,
        'react_id': 1 
    })

    assert response.status_code == 200 

    response = requests.post(config.url + 'message/unreact/v1', json= {
        'token': user2['token'],
        'message_id': mog,
        'react_id': 1 
    })

    assert response.status_code == 200 


