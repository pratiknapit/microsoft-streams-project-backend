import pytest
import requests
import json
from src import config
from src.channel import auth_register_v1

def test_channel_list(): 

    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    auth_id_user_1 = dummy_user_1['auth_user_id']

    resp = requests.post(config.url + 'channels/create', json={
        "token": auth_id_user_1,
        "name": "channel1",
        "is_public": "True"
        })
    
    payload = resp.json()

    assert payload == {"channel_id": 1, "name": "channel1"}

    r = requests.get(config.url + 'channels/list', params = {
        'token': auth_id_user_1
    })

    payload2 = r.json()
    assert payload2 == {
        'channel_id': 1,
        'name': 'channel1'
    }
