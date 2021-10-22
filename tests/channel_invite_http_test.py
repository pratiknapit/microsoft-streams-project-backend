import pytest
import requests
import json
from src import config

@pytest.fixture
def user1():
    email = "test2email@gmail.com"
    password = "TestTest2"
    firstname = "firstname2"
    lastname = "lastname2"
    user = requests.post(config.url + '/auth/register/v2',
                                 json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return json.loads(user.text)


@pytest.fixture
def channel_id():
    channel_name = "Testchannel"
    email = "channelcreator@gmail.com"
    password = "TestTest1"
    firstname = "first"
    lastname = "last"
    owner = requests.post(config.url + '/auth/register/v2',
                                 json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})

    owner = json.loads(owner.text)
    channel_id = requests.post(config.url + 'channels/create', json={
        'token': owner['token'],
        'name': channel_name,
        'is_public': True
    })
    
    return json.loads(channel_id.text)['channel_id']

@pytest.fixture
def channel_owner():

    owner_details = requests.post(config.url + '/auth/login/v2',
                            json={'email': "channelcreator@gmail.com", 'password': "TestTest1"})

    return json.loads(owner_details.text)

@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')
def test_channel_invite(clear, channel_id, channel_owner, user1):
    '''
    A simple test to check channel invite
    '''
    resp = requests.post(config.url + 'channel/invite/v2', json={'token': channel_owner['token'], 'channel_id':channel_id, 'u_id':user1['auth_user_id']})
    assert json.loads(resp.text) == {}

def test_channel_invite_access_error(clear, channel_id, channel_owner, user1):
    resp = requests.post(config.url + 'channel/invite/v2', json={'token': 'bad.input.token', 'channel_id':channel_id, 'u_id':user1['auth_user_id']})
    assert resp.status_code == 403

def test_channel_invite_input_error(clear, channel_id, channel_owner, user1):
    resp = requests.post(config.url + 'channel/invite/v2', json={'token': channel_owner['token'], 'channel_id':channel_id + 1, 'u_id':user1['auth_user_id']})
    assert resp.status_code == 400