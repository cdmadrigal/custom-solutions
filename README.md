# custom-solutions

### Use-Case
Solves the "stage 0" problem around Ansible. Today the Venafi Ansible plugin issues SSH certificates to machines that Ansible has existing SSH connection to. This plugin creates a credential type to create an SSH certificate that may be used to access those machines. 

### Extra
This was tested on an older version of Ansible Tower. But should work on AWX (revamped version of Ansible Tower).
It's important to keep in mind that the user that installed Ansible Tower on the machine (i.e: sudo), must also install this plugin. 

```
Install into each Ansible Tower server with:
yum install -y rust python3-devel git
awx-python -m pip install git+https://github.com/cdmadrigal/custom-solutions
awx-manage setup_managed_credential_types
ansible-tower-service restart
```