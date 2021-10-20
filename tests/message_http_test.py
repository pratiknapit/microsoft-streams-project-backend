import requests
import pytest
import json
import random
import string
from src import config

##############
#message_send#
##############

@pytest.fixture
def token():
    email = "test@unsw.au"
    password = "testPassword"
    firstname = "firstName"
    lastname = "lastName"
    response = requests.post(config.url + '/auth/register/v2', json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    token = response.json()['token']
    return token

@pytest.fixture
def channel_id(token):
    response = requests.post(config.url + '/channels/create/v2', json={'token': token, 'name': 'testChannel01', 'is_public': False})
    return response.json()['channel_id']

@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')


def test_message_too_long(clear, token, channel_id):
    message = ''.join(random.choices(string.ascii_letters, k = 1001))
    response = requests.post(config.url + '/message/send/v2', json={'token': token, 'channel_id': channel_id, 'message': message})
    assert response.status_code == 400

def test_invalid_token(clear, token, channel_id):
    response = requests.post(config.url + '/message/send/v2', json={'token': 'invalid_token', 'channel_id': channel_id, 'message': 'test_message'})
    assert response.status_code == 403

def test_user_not_in_channel(clear, token, channel_id):
    second_token = requests.post(config.url + 'auth/register/v2', json={'email': 'test2@unsw.au', 'password': 'testPassword', 'name_first': 'secondFirst', 'name_last': 'secondLast'})
    second_token = second_token.json()['token']
    response = requests.post(config.url + '/message/send/v2', json={'token': second_token, 'channel_id': channel_id, 'message': 'test_message'})
    assert response.status_code == 403

def test_message_ids_are_unique(clear, token, channel_id):
    m_id1 = requests.post(config.url + '/message/send/v2', json={'token': token, 'channel_id': channel_id, 'message': 'test_message'})
    m_id2 = requests.post(config.url + '/message/send/v2', json={'token': token, 'channel_id': channel_id, 'message': 'test_message'})
    m_id1 = m_id1.json()['message_id']
    m_id2 = m_id2.json()['message_id']
    assert m_id1 != m_id2

def test_message_with_notification(clear, token, channel_id):
    m_id = requests.post(config.url + '/message/send/v2', json={'token': token, 'channel_id': channel_id, 'message': 'test message @firstNamelastName'})
    m_id = m_id.json()['message_id']
    assert isinstance(m_id, int)

def test_invalid_channel_id(clear, token):
    response = requests.post(config.url + '/message/send/v2', json={'token': token, 'channel_id': 'channel_id', 'message': 'test message'})
    assert response.status_code == 400

##############
#message_edit#
##############


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
    return requests.post(config.url + '/message/send/v2', json={'token': admin['token'], 'channel_id': channel['channel_id'], 'message': 'this is a message sent to the other user in the channel.'}).json()


@ pytest.fixture
def dm_message(admin, dm):
    return requests.post(config.url + '/message/senddm/v1', json={'token': admin['token'], 'dm_id': dm['dm_id'], 'message': 'this is a message sent to the other user.'}).json()


def test_invalid_token_dm(dm_message):
    invalid_token = 'invalidtoken123123'
    message_call = requests.put(config.url + '/message/edit/v2', json={
        'token': invalid_token, 'message_id': dm_message, 'message': 'this is an updated message in the dm.'})
    assert message_call.status_code == 403


def test_invalid_token_channel(channel_message):
    invalid_token = 'invalidtoken123123'
    message_call = requests.put(config.url + '/message/edit/v2', json={
        'token': invalid_token, 'message_id': channel_message, 'message': 'this is an updated message in the dm.'})
    assert message_call.status_code == 403


def test_message_incorrect_length_dm(admin, dm_message):
    message_call = requests.put(config.url + '/message/edit/v2', json={
        'token': admin['token'], 'message_id': dm_message, 'message': 1500*'A'})
    assert message_call.status_code == 400


def test_message_incorrect_length_channel(admin, channel_message):
    message_call = requests.put(config.url + '/message/edit/v2', json={
        'token': admin['token'], 'message_id': channel_message, 'message': 1500*'A'})
    assert message_call.status_code == 400


def test_message_sent_by_unauthorised_user_and_not_channel_owner(admin, member, channel_message):
    message_call = requests.put(config.url + '/message/edit/v2', json={'token': member['token'], 'message_id': channel_message['message_id'],
                                                                       'message': 'this is an updated message in the dm.'})
    assert message_call.status_code == 403


def test_success_channel_message(admin, channel, channel_message):
    edit = requests.put(config.url + '/message/edit/v2', json={'token': admin['token'], 'message_id': channel_message['message_id'],
                                                               'message': 'this edit is valid in this channel.'})
    channel_messages = requests.get(config.url + '/channel/messages/v2', params={
        'token': admin['token'], 'channel_id': channel['channel_id'], 'start': 0}).json()
    assert channel_messages['messages'][0]['message'] == 'this edit is valid in this channel.'
    assert edit.status_code == 200


def test_success_dm_message(admin, dm, dm_message):
    edit = requests.put(config.url + '/message/edit/v2', json={'token': admin['token'], 'message_id': dm_message['message_id'],
                                                               'message': 'this edit is valid in this dm.'})
    dm_messages = requests.get(config.url + '/dm/messages/v1', params={
                               'token': admin['token'], 'dm_id': dm['dm_id'], 'start': 0}).json()
    assert dm_messages['messages'][0]['message'] == 'this edit is valid in this dm.'
    assert edit.status_code == 200

################
#message_remove#
################

@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1').json()

@pytest.fixture
def auth_user():
    email = "testmail@gamil.com"
    password = "Testpass12345"
    first_name = "firstname"
    last_name = "lastname"
    token = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()['token']
    return token

@pytest.fixture
def member():
    email = "testmail1@gamil.com"
    password = "Testpass123456"
    first_name = "firstone"
    last_name = "lastone"
    member = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()
    return member

@pytest.fixture
def channel_id(auth_user, member):
    channel_id = requests.post(config.url + '/channels/create/v2', json={
        'token': auth_user,
        'name': "channelName1",
        'is_public': True
    }).json()['channel_id']

    requests.post(config.url + 'channel/join/v2', json={'token': auth_user,
                                                        'channel_id': channel_id})
    return channel_id

@pytest.fixture
def dm_id(auth_user, member):
    dm_id = requests.post(config.url + 'dm/create/v1', json={'token': auth_user,
                                                             'u_ids': [member['auth_user_id']]
                                                             }).json()['dm_id']
    return dm_id

def test_remove_channel_message(clear, auth_user, channel_id):
    message_id = requests.post(config.url + '/message/send/v2',
                                          json={'token': auth_user,
                                                'channel_id': channel_id,
                                                'message': 'Hi'}).json()['message_id']

    response = requests.delete(config.url + 'message/remove/v1',
                               json={'token': auth_user,
                                     'message_id': message_id})
    assert json.loads(response.text) == {}

def test_remove_dm_message(clear, auth_user, dm_id):
    message_id = requests.post(config.url + '/message/senddm/v1',
                               json={'token': auth_user,
                                     'dm_id': dm_id,
                                     'message': 'Hi'}).json()['message_id']

    response = requests.delete(config.url + 'message/remove/v1',
                               json={'token': auth_user,
                                     'message_id': message_id})
    assert json.loads(response.text) == {}


def test_invalid_token(clear):
    response = requests.delete(config.url + 'message/remove/v1', json={'token': "invalid_token", 'message_id': 1})
    assert response.status_code == 403

def test_unauthorised_auth_user(clear, auth_user, member, channel_id, dm_id):
    channel_message_id = requests.post(config.url + '/message/send/v2',
                                       json={'token': auth_user,
                                             'channel_id': channel_id,
                                             'message': 'Hi'}).json()['message_id']

    dm_message_id = requests.post(config.url + '/message/senddm/v1',
                                  json={'token': auth_user,
                                        'dm_id': dm_id,
                                        'message': 'Hi'}).json()['message_id']

    response1 = requests.delete(config.url + 'message/remove/v1',
                                json={'token': member['token'], 'message_id': channel_message_id})
    response2 = requests.delete(config.url + 'message/remove/v1',
                                json={'token': member['token'], 'message_id': dm_message_id})
    assert response1.status_code == 403
    assert response2.status_code == 403

def test_invalid_message_id(clear, auth_user):
    response = requests.delete(config.url + 'message/remove/v1',
                               json={'token': auth_user, 'message_id': 1})
    assert response.status_code == 400





'''
from src.auth import auth_register_v1, auth_login_v1
from src.error import AccessError, InputError
from src.message import message_edit
from src.channels import channels_create_v1
from src.dm import dm_create_v1, dm_messages_v1
from src.message import message_send
from src.channel import channel_messages_v1
'''