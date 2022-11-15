#!/usr/bin/env python
#
# Install into each Ansible Tower server with:
# yum install -y rust python3-devel git
# awx-python -m pip install git+https://github.com/cdmadrigal/custom-solutions
# awx-manage setup_managed_credential_types
# ansible-tower-service restart
#

import os, setuptools

if 'PACKAGE_NAME' not in os.environ:
    print ("ERROR: Please provide environment variable PACKAGE_NAME for the pypi package.")
    package_name = 'ansible_venafi_plugin'
else:
    package_name = os.environ['PACKAGE_NAME']

if 'BUILD_NUMBER' not in os.environ:
    print ("ERROR: Please provide environment variable BUILD_NUMBER for the pypi package.")
else:
    build_version = os.environ['BUILD_NUMBER']

with open('install_requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ansible_venafi_plugin",
    version="0.0.3",
    author='Venafi, Inc.',
    author_email='cris.madrigal@venafi.com',
    description='Custom Ansible credential plugin to retrieve SSH certificates from Venafi TPP.',
    long_description=long_description,
    license='Apache License 2.0',
    keywords='Ansible Venafi TPP SSH certificate',
    url='https://github.com/cdmadrigal/custom-solutions',
    packages=[package_name],
    package_dir={package_name: 'src'},
    include_package_data=True,
    zip_safe=False,
    setup_requires=[],
    install_requires=install_requirements,
    entry_points = {
        'awx.credential_plugins': [
            'venafi_ssh_plugin = ' + package_name + ':venafi_ssh_plugin',
        ]
    }
)
