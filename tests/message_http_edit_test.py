import pytest
import requests
from src import config

@pytest.fixture(autouse=True)
def clear():
    requests.delete(config.url + '/clear/v1')
    yield
    requests.delete(config.url + '/clear/v1')


@pytest.fixture
def admin():
    admin = requests.post(config.url + '/auth/register/v2',
                          json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'first', 'name_last': 'last'})
    admin_details = admin.json()
    return admin_details


@pytest.fixture
def member():
    member = requests.post(config.url + '/auth/register/v2',
                           json={'email': 'test1@unsw.au', 'password': 'password1', 'name_first': 'test1', 'name_last': 'last1'})
    member_1_details = member.json()
    return member_1_details


@pytest.fixture
def channel(admin):
    return requests.post(config.url + '/channels/create/v2', json={'token': admin['token'], 'name': 'channel_1', 'is_public': True}).json()


@ pytest.fixture
def dm(admin, member):
    return requests.post(config.url + '/dm/create/v1', json={'token': admin['token'], 'u_ids': [member['auth_user_id']]}).json()


@ pytest.fixture
def channel_message(admin, channel):
    return requests.post(config.url + '/message/send/v1', json={'token': admin['token'], 'channel_id': channel['channel_id'], 'message': 'this is a message sent to the other user in the channel.'}).json()


def test_invalid_token_channel(channel_message):
    invalid_token = 'invalidtoken123123'
    message_call = requests.put(config.url + '/message/edit/v1', json={
        'token': invalid_token, 'message_id': channel_message['message_id'], 'message': 'this is an updated message in the dm.'})
    assert message_call.status_code == 403

def test_message_incorrect_length_channel(admin, channel_message):
    message_call = requests.put(config.url + '/message/edit/v1', json={
        'token': admin['token'], 'message_id': channel_message['message_id'], 'message': 1500*'A'})
    assert message_call.status_code == 400


def test_message_sent_by_unauthorised_user_and_not_channel_owner(admin, member, channel_message):
    message_call = requests.put(config.url + '/message/edit/v1', json={'token': member['token'], 'message_id': channel_message['message_id'],
                                                                       'message': 'this is an updated message in the dm.'})
    assert message_call.status_code == 403

def test_success_channel_message(admin, channel, channel_message):
    edit = requests.put(config.url + '/message/edit/v1', json={'token': admin['token'], 'message_id': channel_message['message_id'],
                                                               'message': 'this edit is valid in this channel.'})
    response = requests.get(config.url + '/channel/messages/v2', params={
        'token': admin['token'], 'channel_id': channel['channel_id'], 'start': 0}).json()
    assert edit.status_code == 200
    assert response['messages'][0]['message'] == 'this edit is valid in this channel.'