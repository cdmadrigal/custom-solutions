"""Module providing Venafi ssh certificate credential plugin for Ansible Tower."""
import collections

from vcert import venafi_connection, Authentication, SCOPE_SSH, SSHCertRequest
from django.utils.translation import gettext_lazy as _
from .plugin import CertFiles

CredentialPlugin = collections.namedtuple('CredentialPlugin', ['name', 'inputs', 'backend'])

# see: https://docs.ansible.com/ansible-tower/latest/html/userguide/credential_types.html
# inputs will be used to create a new CredentialType() instance
#
# inputs.fields represents fields the user will specify *when they create*
# a credential of this type; they generally represent fields
# used for authentication (URL to the credential management system, any
# fields necessary for authentication, such as an OAuth2.0 token, or
# a username and password). They're the types of values you set up _once_
# in AWX
#
# inputs.metadata represents values the user will specify *every time
# they link two credentials together*
# this is generally _pathing_ information about _where_ in the external
# management system you can find the value you care about i.e.,
#
# "I would like Machine Credential A to retrieve its username using
# Credential-O-Matic B at identifier=some_key"

venafi_ssh_inputs = {
    'fields': [
        {
            'id': 'url',
            'label': 'Server URL',
            'type': 'string',
            'format': 'url',
            'help_text': _('The URL of the Venafi Server.'),
        },
        {
            'id': 'username',
            'label': 'API username',
            'type': 'string',
            "multiline": False,
            'help_text': _('The API username for the Venafi Server.'),
        },
        {
            'id': 'password',
            'label': 'API password',
            'type': 'string',
            'secret': True,
            "multiline": False,
            'help_text': _('The API password of the Venafi Server.'),
        },
        {
            'id': 'cacert',
            'label': 'CA Certificate',
            'type': 'string',
            'multiline': True,
            'help_text': _(
                'The CA certificate used to verify the '
                'API web certificate of the Venafi server.'
            ),
        },
    ],
    'metadata': [
        {
            'id': 'key_id',
            'label': 'SSH Certificate ID',
            'type': 'string',
            'multiline': False,
            'help_text': _(
                'Is a "key identifier" that is logged by the server '
                'when the certificate is used for authentication.'
            ),
        },
        {
            'id': 'valid_principals',
            'label': 'Valid Principals',
            'type': 'string',
            'multiline': False,
            'help_text': _(
                'Valid principals (either usernames or hostnames) '
                'that the certificate should be signed for.'
            ),
        },
        {
            'id': 'public_key',
            'label': 'Unsigned Public Key',
            'type': 'string',
            'multiline': True,
            'help_text': _(
                'Unsigned Public Key of the private key '
                'used for authentication to the client.'
            ),
        },
        {
            'id': 'client_id',
            'label': 'Venafi Client ID',
            'type': 'string',
            'help_text': _(
                'Change the default client id for a custom one. '
                'Make sure this id has been registered on the TPP instance beforehand'
            ),
        },
        {
            'id': 'ca_dn',
            'label': 'CA DN',
            'type': 'string',
            'multiline': False,
            'help_text': _('Certificate Authority DN'),
        },
        {
            'id': 'policy_dn',
            'label': 'Policy DN',
            'type': 'string',
            'multiline': False,
            'help_text': _('Policy DN'),
        },
        {
            'id': 'validity_period',
            'label': 'Validity Period',
            'type': 'string',
            'multiline': False,
            'help_text': _('Time period the certificate is valid for. Default is 15m.'),
        },
    ],
    'required': ['url', 'username', 'password', 'cacert',
                 'key_id', 'valid_principals',  ],
}

def ssh_backend(**kwargs):
    """Connect to Venafi and retrieve a signed public ssh certificate."""

    client_id = kwargs.get(
        'client_id',
        "SSH_IAAS"
    )
    ca_dn = kwargs.get(
        'ca_dn',
        "\\VED\\Policy\\Administration\\CAs\\MSCA - Web Server (1 Year)"
    )
    policy_dn = kwargs.get(
        'policy_dn',
        "\\VED\\Policy\\SSH\\SSH Certificates\\Application 1"
    )
    validity_period = kwargs.get(
        'validity_period',
        "15m"
    )

    with CertFiles(kwargs['cacert']) as cacert:
        connector = venafi_connection(
            url=kwargs['url'],
            user=kwargs['username'],
            password=kwargs['password'],
            http_request_kwargs={'verify': False}
        )

        auth = Authentication(user=kwargs['username'], password=kwargs['password'], scope=SCOPE_SSH)

        auth.client_id = client_id

        connector.get_access_token(auth)

        request = SSHCertRequest(cadn=ca_dn, key_id=kwargs['key_id'], policy_dn=policy_dn)
        request.validity_period = validity_period
        request.set_public_key_data(kwargs['public_key'])

        request.principals = [kwargs['valid_principals']]

        success = connector.request_ssh_cert(request)

        if success:
            response = connector.retrieve_ssh_cert(request)
            return response.certificate_data
        return None


venafi_ssh_plugin = CredentialPlugin(
    'Venafi Signed SSH',
    inputs=venafi_ssh_inputs,
    backend=ssh_backend
)
