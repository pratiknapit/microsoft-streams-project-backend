import pytest
import requests
import json
from src import config

def test_channel_leave_v2():
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + "auth/register/v2", json={
        "email": "pratik7@gmail.com",
        "password": "ronaldo",
        "name_first": "Pratik",
        "name_last": "Napit"
        })
    user1_payload = response.json()
    assert response.status_code == 200

    response2 = requests.post(config.url + "auth/register/v2", json={
        "email": "dummy7@gmail.com",
        "password": "yessir",
        "name_first": "Liam",
        "name_last": "Maverick"
        })
    user2_payload = response2.json()
    assert response2.status_code == 200