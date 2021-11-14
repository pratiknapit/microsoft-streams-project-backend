import pytest
import requests
import json
from src import config

@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1')

@pytest.fixture
def user1(clear):
    email = "testmail@gmail.com"
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
    email = "testmail2@gmail.com"
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
    email = "testmail3@gmail.com"
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

#invalid token 

def test_message_share_access_error(clear, user1, channel1):
    message = requests.post(config.url + '/message/send/v1',
                        json={'token':user1['token'], 'channel_id':channel1['channel_id'], 'message':"TestMessage"})
    msg_id = message.json()['message_id']
    
    resp = requests.post(config.url + 'message/share/v1', json={'token': 'bad.token.input', 'og_message_id':msg_id, 'message':'additional message','channel_id':channel1['channel_id'], 'dm_id':-1})
    
    assert resp.status_code == 403

    response = requests.post(config.url + 'message/share/v1', json= {
        'token': user1['token'],
        'og_message_id': msg_id,
        'message': 'Crypto will bounce after this dip.',
        'channel_id': channel1['channel_id'],
        'dm_id': -1 
    })

    assert response.status_code == 200

#invalid channel 

def test_message_share_invalid_ids0(clear, user1, channel1):
    message = requests.post(config.url + '/message/send/v1',
                        json={'token':user1['token'], 'channel_id':channel1['channel_id'], 'message':"TestMessage"})
    
    assert message.status_code == 200

    msg_id = message.json()
    
    resp = requests.post(config.url + 'message/share/v1', json={'token': user1['token'], 'og_message_id':msg_id['message_id'], 'message':'additional message','channel_id': -1, 'dm_id':-1})
    
    assert resp.status_code == 400

#og message does not refer to a valid message 

def test_message_share_invalid_ids1(clear, user1, channel1):
    message = requests.post(config.url + '/message/send/v1',
                        json={'token':user1['token'], 'channel_id':channel1['channel_id'], 'message':"TestMessage"})
    
    assert message.status_code == 200

    msg_id = message.json()
    
    resp = requests.post(config.url + 'message/share/v1', json={'token': user1['token'], 'og_message_id':msg_id['message_id'], 'message':'additional message','channel_id': 0, 'dm_id': 0})
    
    assert resp.status_code == 400

def test_message_share_invalid_ids2(clear, user1, channel1):
    message = requests.post(config.url + 'message/send/v1',
                        json={'token':user1['token'], 'channel_id':channel1['channel_id'], 'message':"TestMessage"})
    
    assert message.status_code == 200
    
    resp = requests.post(config.url + 'message/share/v1', json={'token': user1['token'], 'og_message_id': -1, 'message':'additional message','channel_id': 0, 'dm_id': 0})
    
    assert resp.status_code == 400

def test_message_share_invalid_ids3(clear, user1, channel1):
    message = requests.post(config.url + 'message/send/v1',
                        json={'token':user1['token'], 'channel_id':channel1['channel_id'], 'message':"TestMessage"})

    assert message.status_code == 200

    msg_id = message.json()

    string_long = 'x' * 1001
    
    resp = requests.post(config.url + 'message/share/v1', json={'token': user1['token'], 'og_message_id':msg_id['message_id'], 'message':string_long,
    'channel_id': channel1['channel_id'], 'dm_id': -1})
    
    assert resp.status_code == 400

#pair of channel and dm_id are valid and the auth user has not
#joined the channel or dm they are trying to share the message to

def test_message_share_to_channel(clear, user1, user2, channel1):
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

    response = requests.post(config.url + 'message/share/v1', json= {
        'token': user1['token'],
        'og_message_id': msg_og['message_id'],
        'message': 'Crypto will bounce after this dip.',
        'channel_id': channel1['channel_id'],
        'dm_id': -1 
    })

    assert response.status_code == 200

def test_message_share_to_diff_channel(clear, user1, user2, channel1, channel2):
    response = requests.post(config.url + 'channel/join/v2', json={
        "token": user2['token'],
        "channel_id": 1
    })

    assert response.status_code == 200

    message_og = requests.post(config.url + 'message/send/v1', json= {
        'token': user1['token'],
        'channel_id': 1,
        'message': 'Yes it will.'
    })

    assert message_og.status_code == 200

    msg_og = message_og.json() 

    response = requests.post(config.url + 'message/share/v1', json= {
        'token': user2['token'],
        'og_message_id': msg_og['message_id'],
        'message': 'Yes it will.',
        'channel_id': channel2['channel_id'],
        'dm_id': -1 
    })

    assert response.status_code == 200 



