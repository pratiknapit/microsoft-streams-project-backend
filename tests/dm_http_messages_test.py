import pytest
import requests
from src import config

@pytest.fixture
def token():
    requests.delete(config.url + 'clear/v1').json()

    email = "testmail@gamil.com"
    password = "Testpass12345"
    first_name = "firstname"
    last_name = "lastname"
    auth_resp = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    })
    token = auth_resp.json()['token']
    return token

@pytest.fixture
def dm_id(token):
    member1 = requests.post(config.url + 'auth/register/v2', json={
        'email': "testmail1@gamil.com",
        'password': "Testpass123456",
        'name_first': "firstone",
        'name_last': "lastone"
    }).json()['auth_user_id']

    member2 = requests.post(config.url + 'auth/register/v2', json={
        'email': "testmail2@gamil.com",
        'password': "Testpass1234567",
        'name_first': "firsttwo",
        'name_last': "lasttwo"
    }).json()['auth_user_id']

    dm_id = requests.post(config.url + 'dm/create/v1', json={
        'token': token,
        'u_ids': [member1, member2]
    }).json()['dm_id']

    return dm_id

@pytest.fixture
def unauthorised_user():
    email = "testmail3@gamil.com"
    password = "Testpass12345"
    first_name = "firstthree"
    last_name = "lastthree"
    token = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()['token']
    return token

def test_invalid_input(token, dm_id):
    resp1 = requests.get(config.url + 'dm/messages/v1', params={
        'token': token,
        'dm_id': "abc",
        'start': 0
    })
    resp2 = requests.get(config.url + 'dm/messages/v1', params={
        'token': token,
        'dm_id': dm_id,
        'start': "ab"
    })

    status_code1 = resp1.status_code
    status_code2 = resp2.status_code
    assert status_code1 == 400
    assert status_code2 == 400

def test_invalid_token(dm_id):
    status_code = requests.get(config.url + 'dm/messages/v1', params={
        'token': "invalid_token",
        'dm_id': dm_id,
        'start': 0
    }).status_code

    assert status_code == 403

def test_invalid_dm_id(token, dm_id):
    status_code = requests.get(config.url + 'dm/messages/v1', params={
        'token': token,
        'dm_id': dm_id + 1,
        'start': 0
    }).status_code

    assert status_code == 400

def test_unauthorised_user(unauthorised_user, dm_id):
    status_code = requests.get(config.url + 'dm/messages/v1', params={
        'token': unauthorised_user,
        'dm_id': dm_id,
        'start': 0
    }).status_code

    assert status_code == 403

def test_invalid_start(token, dm_id):
    status_code = requests.get(config.url + 'dm/messages/v1', params={
        'token': token,
        'dm_id': dm_id,
        'start': 51
    }).status_code

    assert status_code == 400
