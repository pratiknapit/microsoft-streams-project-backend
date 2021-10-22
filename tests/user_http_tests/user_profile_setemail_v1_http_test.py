import requests
import pytest
from src import config
import json



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

def test_already_taken_profile_setemail_v1(clear, dummy_user):
    pass

def test_invalid_profile_setemail_v1(clear, dummy_user):
    user2 = dummy_user
    new_setemail = "incorrectemail"
    registration = requests.put(config.url + "/user/profile/setemail/v1", json={
        'token': user2['token'],
        'email': new_setemail,
    })
    payload = registration.json()
    assert payload['code'] == 400 #InputError
    


def test_valid_profile_setemail_v1(clear, dummy_user):
    user2 = dummy_user
    new_setemail = "smartdummy@gmail.com"
    registration = requests.put(config.url + "/user/profile/setemail/v1", json={
        'token': user2['token'],
        'email': new_setemail,
    })
    payload = registration.json()
    assert payload == {}




   