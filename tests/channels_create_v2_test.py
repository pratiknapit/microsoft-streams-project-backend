import pytest
import requests
import json
from src import config


def test_channel_create_v2_basic(): 
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + "auth/register/v2", json={
        "email": "use4r@gmail.com",
        "password": "dummypass",
        "name_first": "jacky",
        "name_last": "zhu"
        })

    user_payload = response.json()
    assert response.status_code == 200

    response1 = requests.post(config.url + "channels/create", json={
        "token": user_payload['token'],
        "name": "FirstChannel",
        "is_public": "True"
        })

    channel_payload = response1.json()
    assert response1.status_code == 200
    assert channel_payload == {"channel_id": 1}



    
