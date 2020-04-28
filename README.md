# Installation 

`ansible-galaxy collection install a10.acos_cli ` 

## Set Plugin Path 

Add below two lines in /etc/ansible/ansible.cfg File

```bash
cliconf_plugins  = <collection-dir-path>/a10/a10-/plugins/cliconf
terminal_plugins = <collection-dir-path>/a10/acos_collection/plugins/terminal
```

### Alternatives

1. Copy/Move terminal and cli_conf plugin inside 
  * ~/.ansible/plugins
  * /usr/share/ansible/plugins folder

2. Export following environment variables for new session

```bash
export ANSIBLE_CLICONF_PLUGINS=<collection-dir-path>/a10/acos_collection/plugins/cliconf
export ANSIBLE_TERMINAL_PLUGINS=<collection-dir-path>/a10/acos_collection/plugins/terminal
```
	
3. Save this variable in .bashrc File 

```bash
export ANSIBLE_CLICONF_PLUGINS=<collection-dir-path>/a10/acos_collection/plugins/cliconf
export ANSIBLE_TERMINAL_PLUGINS=<collection-dir-path>/a10/acos_collection/plugins/terminal
```

# Usage
        1) You can use the FQCN (namespace.collection_name.module_name)

                tasks:
                 - a10.acos_cli.acos_command:
                        - argument
                 - a10.acos_cli.acos_config
                        - argument

        2) You can use the 'collections' keyword added in Ansible 2.8:

                collections:
                 - a10.acos_cli

                tasks:
                 - acos_command:
                        - argument
                 - acos_config
                        - argument

# Contributing

## Set Collection Path

	
	1) Copy collection folder we got from tarball inside 
					~/.ansible/collections 
							OR 
					/usr/share/ansible/collections folder 
	
	2)  Export following environment variables for new session
		ANSIBLE_COLLECTIONS_PATHS=<path-to-collections-folders>
	
	3) Add below line in /etc/ansible/ansible.cfg File 
		
		collections_paths=<path-to-collection1>:<path-to-collection2>

	4) Keep your playbooks to run in relative to collection 

			|── myplaybook.yml
			├── collections/
			│   └── ansible_collections/
			│               └── a10/
			│                   └── acos_collection/<collection structure lives here>


D] Running ansible-test : 

	$[a10/acos_cli dir]# ansible-test units --venv -v --python 3.6 tests/unit/modules/network/a10/test_acos*.py 
