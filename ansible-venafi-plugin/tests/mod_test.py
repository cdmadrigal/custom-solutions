import pytest
import src
from unittest import mock

def test_venafi_ssh_backend():
    kwargs = {
        'url': 'someurl',
        'username': 'user1',
        'password': 'password1',
        'cacert': 'somecert',
        'key_id': 'somekeyid',
        'valid_principals': 'aprinciple',
        'public_key': 'somekey'
    }
    with mock.patch.object(src, 'ssh_backend') as method_mock:
        method_mock.return_value = 'some_signed_cert'
        token = src.ssh_backend(**kwargs)
        method_mock.assert_called_with(**kwargs)
        assert token == 'some_signed_cert'
