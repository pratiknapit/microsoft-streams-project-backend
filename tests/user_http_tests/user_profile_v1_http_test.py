import requests
import pytest
from src import config
import json
from src.auth import auth_register_v1
from src.other import clear_v1

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
    requests.delete(config.url + 'clear/v1')

def test_invalid_token(clear, dummy_user):
    call = requests.get(config.url + 'user/profile/v1', params={'token' : 'invalidtokencauseisaidso', 'u_id' : dummy_user['auth_user_id']})
    assert call.status_code == 403

def test_invalid_u_id(clear, dummy_user):
    call = requests.get(config.url + 'user/profile/v1', params={'token' : dummy_user['token'], 'u_id' : 0})
    assert call.status_code == 400

def test_user_profile_v1_successful_case(clear, dummy_user):
    result = requests.get(config.url + "user/profile/v1", params={'token' : dummy_user['token'], 'u_id' : dummy_user['auth_user_id']})
    payload = result.json()
    assert payload == {
            'user': {
                "u_id": 2,
                "email": "dummy2@gmail.com",
                "name_first": "Second",
                "name_last": "Two",
                "handle_str": "secondtwo",
                "profile_img_url": []
            }       
    }
