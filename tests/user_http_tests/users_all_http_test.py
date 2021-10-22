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