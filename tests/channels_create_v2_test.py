import pytest
import requests
import json
from src import config


def test_channel_create(): 

    resp = requests.post(config.url + 'channels/create', json={
        "token": 1,
        "name": "channel",
        "is_public": "True"
        })
    
    payload = resp.json()

    assert payload == {"channel_id": 1, "name": "channel"}



    
