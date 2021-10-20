import pytest
import requests
import json
from src import config

def test_echo():
    '''
    A simple test to check echo
    '''
    resp = requests.get(config.url + 'echo', params={'data': 'hello'})
    
    
    assert json.loads(resp.text) == {'data': 'hello'}

    resp2 = requests.get(config.url + 'echo', params={'data': 'echo'})
    assert(resp2.status_code == 400)

