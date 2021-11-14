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
def channel1(user2):
    channel = requests.post(config.url + 'channels/create/v2', json={
        "token": user2['token'],
        "name": "User2Channel1",
        "is_public": True
        })
    return channel.json()

def test_user_stat(clear, user1):
    response = requests.get(config.url + 'user/stats/v1', params={
        'token': user1['token']
    })
    assert response.status_code == 200 

def test_user_stats_valid(clear, user1, channel1):
    requests.post(config.url + '/message/send/v2',
        json={'token':user1['token'], 'channel_id':channel1['channel_id'], 'message':"TestMessage"})

    resp1 = requests.get(config.url + 'user/stats/v1', params={'token': user1['token']})
    resp = resp1.json()['user_stats']
    assert len(resp['channels_joined']) == 1
    assert len(resp['dms_joined']) == 1
    assert len(resp['messages_sent']) == 1
    #assert resp['involvement_rate'] == 1

def test_user_stats_access_error(clear):
    resp = requests.get(config.url + 'user/stats/v1', params={'token': 'bad.token.input'})
    assert resp.status_code == 403

def test_user_stat_function(clear, user1):
    channel = requests.post(config.url + 'channels/create/v2', json={
        "token": user1['token'],
        "name": "User1Channel1",
        "is_public": True
        })

    assert channel.status_code == 200

    response = requests.get(config.url + 'user/stats/v1', params={
        'token': user1['token']
    })

    assert response.status_code == 200

""""
def test_users_stats_valid(clear, user1, channel1):
    requests.post(config.url + '/message/send/v2',
        json={'token':user1['token'], 'channel_id':channel1['channel_id'], 'message':"TestMessage"})

    resp1 = requests.get(config.url + 'users/stats/v1', params={'token': user1['token']})
    resp = resp1.json()['workspace_stats']
    assert len(resp['channels_exist']) == 1
    assert len(resp['dms_exist']) == 1
    assert len(resp['messages_exist']) == 1
    assert resp['utilization_rate'] == 1
    
"""

