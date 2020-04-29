# A10 ACOS CLI Plugin Modules

## Installation 

`ansible-galaxy collection install a10.acos_cli ` 

### 1. Set plugin path 

Add the two lines below to the `/etc/ansible/ansible.cfg` file

```bash
cliconf_plugins  = <collection-dir-path>/a10/acos_cli/plugins/cliconf
terminal_plugins = <collection-dir-path>/a10/acos_cli/plugins/terminal
```

#### 1a. Alternative methods to set path 

1. Copy terminal and cli_conf plugin into one of the following
  * ~/.ansible/plugins
  * /usr/share/ansible/plugins folder

2. Export following environment variables for new session

```bash
export ANSIBLE_CLICONF_PLUGINS=<collection-dir-path>/a10/acos_cli/plugins/cliconf
export ANSIBLE_TERMINAL_PLUGINS=<collection-dir-path>/a10/acos_cli/plugins/terminal
```
	
3. Save this variable in .bashrc File 

```bash
export ANSIBLE_CLICONF_PLUGINS=<collection-dir-path>/a10/acos_cli/plugins/cliconf
export ANSIBLE_TERMINAL_PLUGINS=<collection-dir-path>/a10/acos_cli/plugins/terminal
```

### 2. Add device information to inventory file
```bash
[vthunder]
<vthunder host_name/ip_address>

[vthunder:vars]
ansible_connection=network_cli
ansible_user=<username>
ansible_password=<password>
ansible_network_os=acos
ansible_become_password=<enable_password>
```

**Note: It is recommended to use the Ansible Vault for password storage. Futher information can be found here: https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#using-vault-in-playbooks**

## Usage & Documenation

### Option 1 (Ansbile >=2.8):  Use the 'collections' keyword

```yaml
collections:
  - a10.acos_cli

tasks:
  - acos_command:
    - argument
  - acos_config
    - argument
```

### Option 2: Use the FQCN (namespace.collection_name.module_name)

```yaml
tasks:
  - a10.acos_cli.acos_command:
    - argument
  - a10.acos_cli.acos_config
    - argument
```

### Module Documentation

```
$ ansible-doc -M <collection-dir-path> <module_name>
```

### Plugin Documentation

```
$ ansible-doc -t cliconf acos 
```

### Example Playbooks

Example playbooks can be found here: https://github.com/a10networks/a10-acos-cli/tree/master/examples

## Contributing

### Clone from github

```bash
$ git clone git@github.com:a10networks/a10-acos-cli.git
```

### Methods to set collection path (Only one required) 

1. Copy collection folder we got from tarball inside 
  * ~/.ansible/collections 
  * /usr/share/ansible/collections folder 
	
2. Export following environment variables for new session

```bash
ANSIBLE_COLLECTIONS_PATHS=<path-to-collections-folders>
```
	
3. Add below line in /etc/ansible/ansible.cfg File 

```bash	
collections_paths=<path-to-collection1>:<path-to-collection2>
```

4. Keep your playbooks to run in relative to collection 

```
	|── myplaybook.yml
	├── collections/
	│   └── ansible_collections/
	│               └── a10/
	│                   └── acos_cli/<collection structure lives here>
```

## Testing

```bash
$ ansible-test units --venv -v --python 3.6 tests/unit/modules/network/a10/test_acos*.py 
```

## Issues and Inquiries
For all issues, please send an email to support@a10networks.com 

For general inquiries, please send an email to opensource@a10networks.com
