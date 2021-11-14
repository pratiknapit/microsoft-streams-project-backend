import pytest
import requests
import json
from src import config

@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1')

@pytest.fixture
def user1(clear):
    user1 = requests.post(config.url + "auth/register/v2", json={
        "email": "pratik7@gmail.com",
        "password": "ronaldo",
        "name_first": "Pratik",
        "name_last": "Napit"
        })
    return user1.json()

@pytest.fixture
def user2():
    user2 = requests.post(config.url + "auth/register/v2", json={
        "email": "afsadsf7@gmail.com",
        "password": "random123123",
        "name_first": "John",
        "name_last": "Dummmy"
        })
    return user2.json()

@pytest.fixture
def user3():
    user3 = requests.post(config.url + "auth/register/v2", json={
        "email": "computernerd45@gmail.com",
        "password": "bestgate",
        "name_first": "RandomGuy",
        "name_last": "Yummy"
        })
    return user3.json()

@pytest.fixture
def channel1(user1):
    channel = requests.post(config.url + 'channels/create/v2', json={
        "token": user1['token'],
        "name": "FirstChannel",
        "is_public": True
        })
    return channel.json()

def test_invalid_token_add(clear, user1, channel1, user2):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/addowner/v1', json={
        "token": "random_token",
        "channel_id": channel1['channel_id'],
        "u_id": user2['auth_user_id']
    })
    assert response.status_code == 403

def test_invalid_token_remove(clear, user1, channel1, user2):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/addowner/v1', json={
        "token": "random_token",
        "channel_id": channel1['channel_id'],
        "u_id": user2['auth_user_id']
    })
    assert response.status_code == 403

def test_invalid_channel_add(clear, user1, channel1, user2):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/addowner/v1', json={
        "token": user1['token'],
        "channel_id": "random_channel_id",
        "u_id": user2['auth_user_id']
    })
    assert response.status_code == 400

def test_invalid_channel_remove(user1, channel1, user2):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/removeowner/v1', json={
        "token": user1['token'],
        "channel_id": "random_channel_id",
        "u_id": user2['auth_user_id']
    })
    assert response.status_code == 400

def test_invalid_user_add(clear, user1, channel1, user2):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/addowner/v1', json={
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "u_id": "random_user"
    })
    assert response.status_code == 400

def test_invalid_user_remove(clear, user1, channel1, user2):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/removeowner/v1', json={
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "u_id": "random_user"
    })
    assert response.status_code == 400

def test_user_is_not_channel_member_add(clear, user1, channel1, user2, user3):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/addowner/v1', json={
        "token": user3['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user2['auth_user_id']
    })
    assert response.status_code == 400

def test_user_is_not_channel_member_remove(clear, user1, channel1, user2, user3):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/removeowner/v1', json={
        "token": user3['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user2['auth_user_id']
    })
    assert response.status_code == 400

def test_user_is_already_channel_owner_add(clear, user1, channel1, user2, user3):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/addowner/v1', json={
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user1['auth_user_id']
    })
    assert response.status_code == 400

def test_user_is_already_channel_owner_remove(clear, user1, channel1, user2, user3):
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'channel/removeowner/v1', json={
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user1['auth_user_id']
    })
    assert response.status_code == 400

def test_no_owner_permission_add(clear, user1, channel1, user2, user3):
    response = requests.post(config.url + 'channel/join/v2', json={
        "token": user3['token'],
        "channel_id": channel1['channel_id']
    })

    response = requests.post(config.url + 'channel/addowner/v1', json={
        "token": user2['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user3['auth_user_id']
    })
    assert response.status_code == 403

def test_no_owner_permission_remove(clear, user1, channel1, user2, user3):
    response = requests.post(config.url + 'channel/join/v2', json={
        "token": user3['token'],
        "channel_id": channel1['channel_id']
    })

    response = requests.post(config.url + 'channel/removeowner/v1', json={
        "token": user2['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user3['auth_user_id']
    })
    
    assert response.status_code == 403

def test_channel_add_remove_owner1(clear, user1, user2, channel1):
    r1 = requests.post(config.url + 'channel/join/v2', json={
        "token": user2['token'],
        "channel_id": channel1['channel_id']
    })
    assert r1.status_code == 200

    r2 = requests.post(config.url + 'channel/addowner/v1', json={
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user2['auth_user_id']
    })
    assert r2.status_code == 200

    r3 = requests.post(config.url + 'channel/removeowner/v1', json={
        "token": user1['token'],
        "channel_id": channel1['channel_id'],
        "u_id": user2['auth_user_id']
    })
    assert r3.status_code == 200

# Jacky's tests
@pytest.fixture
def owner():
    email = "testmail1@gamil.com"
    password = "Testpass12345"
    first_name = "firstone"
    last_name = "lastone"
    user_info = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()
    return user_info

@pytest.fixture
def member():
    email = "testmail2@gamil.com"
    password = "Testpass123456"
    first_name = "firsttwo"
    last_name = "lasttwo"
    user_info = requests.post(config.url + 'auth/register/v2', json={
        'email': email,
        'password': password,
        'name_first': first_name,
        'name_last': last_name
    }).json()
    return user_info

@pytest.fixture
def channel_id(owner, member):
    channel_id = requests.post(config.url + 'channels/create/v2', json={
        'token': owner['token'],
        'name': "channelName1",
        'is_public': True
    }).json()['channel_id']

    requests.post(config.url + 'channel/join/v2', json={
        'token': member['token'],
        'channel_id': channel_id
    })
    return channel_id

def test_invalid_token(clear, channel_id, member):
    status_code = requests.post(config.url + 'channel/removeowner/v1', json={
        'token': "invalid_token",
        'channel_id': channel_id,
        'u_id': member['auth_user_id']
    }).status_code

    assert status_code == 403

def test_invalid_channel_id(clear, owner, channel_id, member):
    status_code = requests.post(config.url + 'channel/removeowner/v1', json={
        'token': owner['token'],
        'channel_id': channel_id + 1,
        'u_id': member['auth_user_id']
    }).status_code

    assert status_code == 400

def test_user_not_owner(clear, owner, channel_id):
    status_code = requests.post(config.url + 'channel/removeowner/v1', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'u_id': 5
    }).status_code

    assert status_code == 400

def test_remove_only_owner(clear, owner, channel_id):
    status_code = requests.post(config.url + 'channel/removeowner/v1', json={
        'token': owner['token'],
        'channel_id': channel_id,
        'u_id': owner['auth_user_id']
    }).status_code

    assert status_code == 400

'''
def test_token_not_owner(clear, channel_id, owner):
    not_owner = requests.post(config.url + 'auth/register/v2', json={
        'email': "teste23mail@gmail.com",
        'password': "password111",
        'name_first': "firstthree",
        'name_last': "lastthree"
    }).json()['token']

    status_code = requests.post(config.url + 'channel/removeowner/v1', json={
        'token': not_owner,
        'channel_id': channel_id,
        'u_id': owner['auth_user_id']
    }).status_code

    assert status_code == 403
'''

@pytest.fixture
def create_admin():
    admin = requests.post(config.url + '/auth/register/v2',
                          json={'email': 'test@unsw.au', 'password': 'password', 'name_first': 'first', 'name_last': 'last'})
    admin_details = admin.json()
    return admin_details


@pytest.fixture
def create_member_1():
    member = requests.post(config.url + '/auth/register/v2',
                           json={'email': 'test1@unsw.au', 'password': 'password1', 'name_first': 'test1', 'name_last': 'last1'})
    member_1_details = member.json()
    return member_1_details


def test_invalid_token(clear, create_admin, create_member_1):

    admin_invalid_token = 'invalidtoken123123'
    admin = create_admin
    member = create_member_1
    channel = requests.post(config.url + '/channels/create/v2',
                            json={'token': admin['token'], 'name': 'channel_1', 'is_public': True})
    channel_id = channel.json()
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': admin_invalid_token, 'channel_id': channel_id['channel_id'], 'u_id': member['auth_user_id']})
    assert addowner.status_code == 403


def test_invalid_channel(clear, create_admin, create_member_1):
    admin = create_admin
    member = create_member_1
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': admin['token'], 'channel_id': 1, 'u_id': member['auth_user_id']})
    assert addowner.status_code == 400


def test_user_nonexistent(clear, create_admin):
    admin = create_admin
    channel = requests.post(config.url + '/channels/create/v2',
                            json={'token': admin['token'], 'name': 'channel_1', 'is_public': True})
    channel_id = channel.json()
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': admin['token'], 'channel_id': channel_id['channel_id'], 'u_id': 10})
    assert addowner.status_code == 400


def test_user_already_owner(clear, create_admin, create_member_1):
    admin = create_admin
    channel = requests.post(config.url + '/channels/create/v2',
                            json={'token': admin['token'], 'name': 'channel_1', 'is_public': True})
    channel_id = channel.json()
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': admin['token'], 'channel_id': channel_id['channel_id'], 'u_id': admin['auth_user_id']})
    assert addowner.status_code == 400

'''
def test_not_owner_of_channel_or_dreams(clear, create_admin, create_member_1):
    admin = create_admin
    member_1 = create_member_1
    member_2 = requests.post(config.url + '/auth/register/v2',
                             json={'email': 'test2@unsw.au', 'password': 'password2', 'name_first': 'test2', 'name_last': 'last2'})
    member_2_details = member_2.json()
    channel = requests.post(config.url + '/channels/create/v2',
                            json={'token': admin['token'], 'name': 'channel_1', 'is_public': True})
    channel_id = channel.json()
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': member_1['token'], 'channel_id': channel_id['channel_id'], 'u_id': member_2_details['auth_user_id']})
    assert addowner.status_code == 403
'''
'''
def test_successful_addowner(clear, create_admin, create_member_1):
    admin = create_admin
    member = create_member_1
    channel = requests.post(config.url + '/channels/create/v2',
                            json={'token': admin['token'], 'name': 'channel_1', 'is_public': True})
    channel_details = channel.json()
    addowner = requests.post(config.url + '/channel/addowner/v1',
                             json={'token': admin['token'], 'channel_id': channel_details['channel_id'], 'u_id': member['auth_user_id']})
    assert addowner.status_code == 200
'''