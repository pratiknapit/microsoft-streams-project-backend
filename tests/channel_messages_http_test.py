import pytest
import requests
from src import config

@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')

@pytest.fixture
def token():
    email = "testmail@gamil.com"
    password = "Testpass12345"
    first_name = "firstname"
    last_name = "lastname"
    auth_resp = requests.post(config.url + '/auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()
    token = auth_resp['token']
    return token

@pytest.fixture
def channel_id(token):
    resp = requests.post(config.url + '/channels/create', json={
        'token': token,
        'name': "channelName1",
        'is_public': True
    }).json()

    channel_id = resp['channel_id']
    return channel_id
'''
def test_invalid_input(token, channel_id):
    resp1 = requests.get(config.url + '/channel/messages/v2', params={
        'token': token,
        'channel_id': "abc",
        'start': 0
    })
    resp2 = requests.get(config.url + '/channel/messages/v2', params={
        'token': token,
        'channel_id': channel_id,
        'start': "ab"
    })

    status_code1 = resp1.status_code
    status_code2 = resp2.status_code
    assert status_code1 == 400
    assert status_code2 == 400
'''
def test_invalid_token(clear, channel_id):
    resp = requests.get(config.url + '/channel/messages/v2', params={
        'token': "invalid_token",
        'channel_id': channel_id,
        'start': 0
    })

    status_code = resp.status_code
    assert status_code == 403

def test_invalid_channel_id(clear, token, channel_id):
    resp = requests.get(config.url + '/channel/messages/v2', params={
        'token': token,
        'channel_id': channel_id + 1,
        'start': 0
    })

    status_code = resp.status_code
    assert status_code == 400

def test_user_not_in_channel(clear, channel_id):
    not_member_token = requests.post(config.url + 'auth/register/v2', json={
        'email': 'test2@unsw.au',
        'password': 'testPassword',
        'name_first': 'secondFirst',
        'name_last': 'secondLast'})
    not_member_token = not_member_token.json()['token']

    resp = requests.get(config.url + '/channel/messages/v2', params={
        'token': not_member_token,
        'channel_id': channel_id,
        'start': 0
    })
    status_code = resp.status_code
    assert status_code == 403

def test_invalid_start(clear, token, channel_id):
    resp = requests.get(config.url + '/channel/messages/v2', params={
        'token': token,
        'channel_id': channel_id,
        'start': 51
    })

    status_code = resp.status_code
    assert status_code == 400

def test_messages(clear, token, channel_id):
    for i in range(3):
        requests.post(config.url + '/message/send/v1', json={
            'token': token,
            'channel_id': channel_id,
            'message': f"{i}"
        })

    messages_dict = requests.get(config.url + '/channel/messages/v2', params={
            'token': token,
            'channel_id': channel_id,
            'start': 0
        })
    resp_dict = messages_dict.json()
    assert messages_dict.status_code == 200
    assert 'messages' and 'start' and 'end' in resp_dict