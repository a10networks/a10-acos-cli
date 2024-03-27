## Introduction
Thunder® ADCs (Application Delivery Controllers) are high-performance solutions to accelerate and optimize critical applications to ensure delivery and reliability.

A10 Ansible ACOS CLI modules is a custom plugin to do configurations on Thunder via CLI commands. It includes example playbooks to apply on hardware and virtual appliances.

We only support Ansible Suite version >=2.9

## Support Matrix

| ACOS CLI Version | Ansible Version | Ansible Tower | Ansible Automation Platform |Ansible Netcomm |
| :--------: | :-------: | :-------:  |:-------:  |:-------:  |
| `1.2.1` |  `2.9.x`, `2.13.x`, `2.14.x`, `2.15.x`, `2.16.x` | `17.1.x` |  Not Support | `>=2.0.0,<3.0.0` |
| `2.0.0` |  `2.9.x`, `2.13.x`, `2.14.x`, `2.15.x`, `2.16.x` | `17.1.x` |  `2.4.4` | `>=3.0.0,=<6.0.0` |

## How it works
   1. Install Ansible on your local OS.
   2. Search required Ansible configuration from examples.
   3. Execute Ansible playbooks to apply thunder configuration.
   4. Verify thunder configuration after ansible playbook is applied.

   Please refer below sections for more details.

## How to install Ansbile Suite on Ubuntu
To install Ansible Suite on Ubuntu, Run the following command to download and install the latest version of Ansible:

```
apt install ansible
```

## How to install Ansbile Suite on MacOS
To install Ansible on MacOS, Run the following command to download and install the latest version of Ansible:

```
brew install ansible
```

## How to install A10 Ansible CLI Modules
a10-acos-cli is collection of custom ansible modules crated by a10Networks. It can be install using following ways, it is assumed that ansible suite is already installed and configured.

### 1. Install from galaxy hub

`ansible-galaxy collection install a10.acos_cli-* `

Be sure to note the collection path found within the output of the above command. For example:
```bash
$ ansible-galaxy collection install a10.acos_cli-*
Process install dependency map
Starting collection install process
Installing 'a10.acos_cli:*.*.*' to '/root/.ansible/collections/ansible_collections/a10/acos_cli'
Installing 'ansible.netcommon:6.0.0' to '/root/.ansible/collections/ansible_collections/ansible/netcommon'
```

In this example the collection directory path is: `/root/.ansible/collections/ansible_collections/`


### 2. Install from the Github repository

  ~~~
  git clone https://github.com/a10networks/a10-acos-cli.git
  cd a10-acos-cli
  ansible-galaxy collection build
  ansible-galaxy collection install a10-acos_cli*.tar.gz -f
  ~~~

## How to configure A10 Ansible ACOS CLI Modules

#### 1. Set plugin path

Add the two lines below to the `/etc/ansible/ansible.cfg` file

```bash
cliconf_plugins  = <collection-dir-path>/a10/acos_cli/plugins/cliconf
terminal_plugins = <collection-dir-path>/a10/acos_cli/plugins/terminal
```

#### 2. Alternative methods to set path

1. Copy terminal and cli_conf plugin into one of the following
  * ~/.ansible/plugins
  * /usr/share/ansible/plugins folder

2. Export following environment variables for new session

```bash
[defaults]
export ANSIBLE_CLICONF_PLUGINS=<collection-dir-path>/a10/acos_cli/plugins/cliconf
export ANSIBLE_TERMINAL_PLUGINS=<collection-dir-path>/a10/acos_cli/plugins/terminal
```

3. Save this variable in .bashrc File

```bash
[defaults]
export ANSIBLE_CLICONF_PLUGINS=<collection-dir-path>/a10/acos_cli/plugins/cliconf
export ANSIBLE_TERMINAL_PLUGINS=<collection-dir-path>/a10/acos_cli/plugins/terminal
```

**Note: It is recommended to use the Ansible Vault for password storage. Futher information can be found here: https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#using-vault-in-playbooks**

## How to use A10 Ansible ACOS CLI Module Collections
Ansible collections are a powerful way to organize and distribute Ansible content, such as roles, modules, and plugins.

## Creating / updating a resource

Any of the following method can be used to create and run playbooks.

### 1: Use the 'collections' keyword

```yaml
collections:
  - a10.acos_cli

tasks:
  - acos_command:
    - argument
  - acos_config
    - argument
```

### 2: Use the Fully Qualified Collection Name (namespace.collection_name.module_name)

```yaml
tasks:
  - a10.acos_cli.acos_command:
    - argument
  - a10.acos_cli.acos_config
    - argument
```

## How to search Ansible module configurations
To search for a Ansible Module Configuration in the existing examples, perform the following steps:

  1. Search the required Ansible Module configuration script directory, navigate to examples.

     **Example:**

      If you want to apply the configuration on Thunder, search for the acos_config.yml playbook.

  2. Open the Ansible playbook from the directory.

     **Example:**

      Open acos_config.yml playbook under the examples directory.

  3. Update the **hosts** parameter in playbook and add, modify, or remove the Ansible module configuration parameters and their corresponding values as appropriate.

  ```
  - name: RUN COMMAND FOR CONFIGURE FILE
    hosts: "{{desired_inventory_group}}"
    gather_facts: false
    become: True
    tasks:
        - name: run lines
          a10.acos_cli.acos_config:
            lines:
            - ip dns primary 10.8.4.35
            - slb template http template12
            - slb server servertest 20.20.15.147
            - port 74 tcp
            - slb server serv13 20.15.27.126
  ```

  4. Save the playbook.


## How to execute Ansible playbooks from CLI
### 1. With Inventory file
Sample Inventory file:

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


Use the following command to run the playbook:
```shell
ansible-playbook -i <path_to_inventory> <name_of_playbook>
```

## How to verify on Thunder

  To verify the applied configurations, follow below steps:

  1. SSH into the Thunder device using your username and password.
  2. Once connected, enter the following commands:

     1. `enable`

        ![image](https://github.com/smundhe-a10/terraform-provider-thunder/assets/107971633/7e532cee-fa8e-4af7-aa50-da56a24dd4c3)


     3. `show running-config`

        ![image](https://github.com/smundhe-a10/terraform-provider-thunder/assets/107971633/ae37e53d-c650-43f0-b71f-2416f4e5d65a)

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

## Testing

```bash
$ ansible-test units --venv -v --python 3.6 tests/unit/modules/network/a10/test_acos*.py
```

## License
[APACHE LICENSE VERSION 2.0](LICENSE.txt)

All rights reserved @A10 Networks Inc.

## Open Source Disclaimer

	For more information, please refer [/OPEN-SOURCE-Notice.pdf]

## Report a Issue

Please raise issue in github repository. Please include the Ansible playbook or ansible module files that demonstrates the bug and the command output and stack traces will be helpful.

## Support
For all issues, please send an email to support@a10networks.com with subject "a10-acos-cli"
