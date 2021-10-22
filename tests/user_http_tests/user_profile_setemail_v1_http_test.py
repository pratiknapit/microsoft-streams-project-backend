import requests
import pytest
from src.config import url
import json

@pytest.fixture
def dummy_user():
    requests.delete(f"{url}/clear/v1") # Clear the data
    requests.post(f"{url}/auth/register/v1", json={
        "email": "dummy1@gmail.com",
        "password": "password1",
        "name_first": "First",
        "name_last": "One",
    })
    user2 = requests.post(f"{url}/auth/register/v1", json={
        "email": "dummy2@gmail.com",
        "password": "password2",
        "name_first": "Second",
        "name_last": "Two",
    })
    payload = user2.json
    return payload


def test_already_taken_profile_setemail_v1(dummy_user):
    pass

def test_invalid_profile_setemail_v1(dummy_user):

    user2 = dummy_user
    new_setemail = "incorrectemail"
    registration = requests.put(f"{url}/user/profile/setemail/v1", json={
        'token': user2['token'],
        'email': new_setemail,
    })
    payload = registration.json()
    assert payload['code'] == 400 #InputError


def test_valid_profile_setemail_v1(dummy_user):
    user2 = dummy_user
    new_setemail = "smartdummy@gmail.com"
    registration = requests.put(f"{url}/user/profile/setemail/v1", json={
        'token': user2['token'],
        'email': new_setemail,
    })
    payload = registration.json()
    assert payload == {}




   