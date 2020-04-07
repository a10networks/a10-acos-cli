# Download the Collection Using following Command 

` ansible-galaxy collection install a10.acos_collection ` 

-----------------------------------------------------------------------------------------------------

## How to Use Collection : 

A] Set the plugin path using any one of the following way:
	
	1) Copy/Move terminal and cli_conf plugin inside 
	   ~/.ansible/plugins 			
				OR 
	   /usr/share/ansible/plugins folder
	
	2) Add below two lines in /etc/ansible/ansible.cfg File 

		cliconf_plugins  = <collection-dir-path>/a10/acos_collection/plugins/cliconf
		terminal_plugins = <collection-dir-path>/a10/acos_collection/plugins/terminal
	
	3) Export following environment variables for new session

		export ANSIBLE_CLICONF_PLUGINS=<collection-dir-path>/a10/acos_collection/plugins/cliconf
		export ANSIBLE_TERMINAL_PLUGINS=<collection-dir-path>/a10/acos_collection/plugins/terminal
 	
 	4) Save this variable in .bashrc File 

		export ANSIBLE_CLICONF_PLUGINS=<collection-dir-path>/a10/acos_collection/plugins/cliconf
		export ANSIBLE_TERMINAL_PLUGINS=<collection-dir-path>/a10/acos_collection/plugins/terminal

-----------------------------------------------------------------------------------------------------

B] Accessing/Using Collection (Use Any one of the way ) :
	
	1) Copy/Move - Collection folder we got from tarball inside 
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

-----------------------------------------------------------------------------------------------------
C] How to access Collection Modules inside Playbook: 
	
	1) You can use the FQCN (namespace.collection_name.module_name) 
		
		tasks:
		 - a10.acos_collection.acos_command:
		 	- argument 
		 - a10.acos_collection.acos_config
		 	- argument 

	2) You can use the 'collections' keyword added in Ansible 2.8:
		
		collections:
		 - a10.acos_colllection

		tasks:
		 - acos_command:
		 	- argument 
		 - acos_config
		 	- argument 
-----------------------------------------------------------------------------------------------------
D] Running ansible-test : 

	$[a10/acos_collection dir]# ansible-test units --venv -v --python 3.6 tests/unit/modules/network/a10/test_acos*.py 
