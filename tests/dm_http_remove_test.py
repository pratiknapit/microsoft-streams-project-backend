import pytest
import requests
import json
from src import config

@pytest.fixture
def user0():
    email = "testemail@gmail.com"
    password = "TestTest"
    firstname = "firstname"
    lastname = "lastname"
    user = requests.post(config.url + '/auth/register/v2',
                                 json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return json.loads(user.text)

@pytest.fixture
def owner():
    email = "dmcreator@gmail.com"
    password = "TestTest1"
    firstname = "first"
    lastname = "last"
    user = requests.post(config.url + '/auth/register/v2',
                                 json={'email': email, 'password': password, 'name_first': firstname, 'name_last': lastname})
    return json.loads(user.text)

@pytest.fixture
def dm(owner, user0):
    dm = requests.post(config.url + '/dm/create/v1',
                        json={'token': owner['token'], 'u_ids':[user0['auth_user_id']]})
    return json.loads(dm.text)

@pytest.fixture
def owner_token():
    owner = requests.post(config.url + '/auth/login/v2',
                        json={'email': "dmcreator@gmail.com", 'password': "TestTest1"})
    return json.loads(owner.text)['token']

@pytest.fixture
def clear():
    requests.delete(config.url + '/clear/v1')

def test_dm_remove(clear, dm, owner_token):
    resp = requests.delete(config.url + 'dm/remove/v1', json={'token': owner_token, 'dm_id':dm['dm_id']})
    assert resp.json() == {}

def test_dm_remove_access_error(clear, dm, owner_token):
    resp = requests.delete(config.url + 'dm/remove/v1', json={'token': 'bad.token.input', 'dm_id':dm['dm_id']})
    assert resp.status_code == 403

def test_dm_remove_input_error(clear, dm, owner_token):
    resp = requests.delete(config.url + 'dm/remove/v1', json={'token': owner_token, 'dm_id':dm['dm_id'] + 1})
    assert resp.status_code == 400

def test_dm_remove_valid(clear):
    """
    This function test the valid case of dm_remove_v1
    """

    # Users information to be pass in as json
    user1_data = {
        "email": "jackyzhue@gmail.com",
        "password": "password123",
        "name_first": "jacky",
        "name_last": "zhu",
    }

    user2_data = {
        "email": "pratikscd@gmail.com",
        "password": "1122334",
        "name_first": "pratik",
        "name_last": "napit",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(config.url + "/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    auth_id1 = payload["auth_user_id"]
    
    auth_user2_info = requests.post(config.url + "/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()

    token2 = payload["token"]

    u_ids = [auth_id1]
    dm_response = requests.post(config.url + "/dm/create/v1", json = {
        "token": token2, 
        "u_ids": u_ids
    })

    payload = dm_response.json()
    dm_id = payload["dm_id"]

    dm_response = requests.delete(config.url + "/dm/remove/v1", json = {
        "token": token2,
        "dm_id": dm_id
    })
  
 
    assert dm_response.status_code == 200

    

def test_dm_remove_invalid_dm(clear):
    """
    This function test the invalid DM channel ID case
    """

    # Users information to be pass in as json
    user1_data = {
        "email": "jackyzhue@gmail.com",
        "password": "password123",
        "name_first": "jacky",
        "name_last": "zhu",
    }

    user2_data = {
        "email": "safwanwef@gmail.com",
        "password": "123wqfe",
        "name_first": "safwan",
        "name_last": "sadge",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(config.url + "/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    
    auth_id1 = payload["auth_user_id"]
    
    auth_user2_info = requests.post(config.url + "/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
   
    token2 = payload["token"]

    u_ids = [auth_id1]
    dm_response = requests.post(config.url + "/dm/create/v1", json = {
        "token": token2, 
        "u_ids": u_ids
    })


    invalid_dm = 900

    dm_response = requests.delete(config.url + "/dm/remove/v1", json = {
        "token": token2,
        "dm_id": invalid_dm
    })

    # Test invalid DM ID by checking if 400 status code is raised
    assert dm_response.status_code == 400

def test_dm_remove_not_owner(clear):
    """
    This function test the invalid DM channel ID case
    """


    # Users information to be pass in as json
    user1_data = {
        "email": "jackyzhuwe@gmail.com",
        "password": "pasewrt",
        "name_first": "jacky",
        "name_last": "zhu",
    }

    user2_data = {
        "email": "pratiksaf@gmail.com",
        "password": "1234567",
        "name_first": "pratik",
        "name_last": "safwan",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(config.url + "/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]
    
    
    auth_user2_info = requests.post(config.url + "/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    auth_id2 = payload["auth_user_id"]
    token2 = payload["token"]

    u_ids = [auth_id2]
    dm_response = requests.post(config.url + "/dm/create/v1", json = {
        "token": token1, 
        "u_ids": u_ids
    })

    payload = dm_response.json()
    dm_id = payload["dm_id"]
   

    dm_response = requests.delete(config.url + "/dm/remove/v1", json = {
        "token": token2,
        "dm_id": dm_id
    })

    # Test invalid original owner by checking if 403 status code is raised
    assert dm_response.status_code == 403

def test_dm_remove_invalid_auth(clear):
    """
    This function test the invalid token case
    """

    # Users information to be pass in as json
    user1_data = {
        "email": "jackyzhuwe@gmail.com",
        "password": "passwwqef23",
        "name_first": "jacky",
        "name_last": "zhu",
    }

    user2_data = {
        "email": "coolguy@gmail.com",
        "password": "123wq56",
        "name_first": "cool",
        "name_last": "ghuy",
    }

    # Call other routes to create the data and store in data structure
    auth_user1_info = requests.post(config.url + "/auth/register/v2", json = user1_data)
    payload = auth_user1_info.json()
    token1 = payload["token"]
    
    
    auth_user2_info = requests.post(config.url + "/auth/register/v2", json = user2_data)
    payload = auth_user2_info.json()
    auth_id2 = payload["auth_user_id"]
    

    u_ids = [auth_id2]
    dm_response = requests.post(config.url + "/dm/create/v1", json = {
        "token": token1, 
        "u_ids": u_ids
    })

    payload = dm_response.json()
    dm_id = payload["dm_id"]
    invalid_token = 990
   

    dm_response = requests.delete(config.url + "/dm/remove/v1", json = {
        "token": invalid_token,
        "dm_id": dm_id
    })

    # Test invalid token by checking if 403 status code is raised
    assert dm_response.status_code == 403