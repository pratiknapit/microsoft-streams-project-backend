import requests
import pytest
from src import config
import json
import urllib
from src.data_store import is_valid_token

@pytest.fixture
def dummy_user():
    requests.post(config.url + "/auth/register/v2", json={
        "email": "dummy1@gmail.com",
        "password": "password1",
        "name_first": "First",
        "name_last": "One",
    })
    user2 = requests.post(config.url + "/auth/register/v2", json={
        "email": "dummy2@gmail.com",
        "password": "password2",
        "name_first": "Second",
        "name_last": "Two",
    })

    payload = user2.json()
    return payload

@pytest.fixture
def clear():
    requests.delete(config.url + "/clear/v1")

def test_user_all_valid(clear, dummy_user):

    result = requests.get(config.url + "/users/all/v1?", params={'token' : dummy_user['token']})
    payload = result.json()
    assert payload == {
        'users': [
            {
                "u_id": 1,
                "email": "dummy1@gmail.com",
                "name_first": "First",
                "name_last": "One",
                "handle_str": "firstone"              
            },
            {
                "u_id": 2,
                "email": "dummy2@gmail.com",
                "name_first": "Second",
                "name_last": "Two",
                "handle_str": "secondtwo"    
            }
        ]
    }

def test_user_all_invalid_token(clear):
    invalid_token = 'incorrectoken'
    query = urllib.parse.urlencode({
        'token': invalid_token
    })
    result = requests.get(config.url + "/users/all/v1?{query}")
    payload = result.json()
    assert payload['code'] == 403 # AccessError
