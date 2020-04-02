# Download the Collection Using following Command 

` ansible-galaxy collection install my_namespace.my_collection ` 

## How to Use Collection : 

A] Set the plugin path using any one of the following ways 
	
	1) Copy/Move - terminal and cli_conf plugin inside ~/.ansible/plugins or 
	   /usr/share/ansible/plugins folder 
	
	2) Add below two lines in /etc/ansible/ansible.cfg File 

		cliconf_plugins  = <collection-dir-path>/a10/acos_collection/plugins/cliconf
		terminal_plugins = <collection-dir-path>/a10/acos_collection/plugins/terminal
	
	3) Run Below two commands every time you start new terminal session 

		export ANSIBLE_CLICONF_PLUGINS=<collection-dir-path>/a10/acos_collection/plugins/cliconf
		export ANSIBLE_TERMINAL_PLUGINS=<collection-dir-path>/a10/acos_collection/plugins/terminal
 	
 	4) Save this variable in .bashrc File 

		export ANSIBLE_CLICONF_PLUGINS=<collection-dir-path>/a10/acos_collection/plugins/cliconf
		export ANSIBLE_TERMINAL_PLUGINS=<collection-dir-path>/a10/acos_collection/plugins/terminal

B] Accessing/Using Collection (Use Any one of the way ) :
	
	1) Copy/Move - Collection folder we got from tarball inside ~/.ansible/plugins 
		or /usr/share/ansible/collections folder 
	
	2) Run Below two commands every time you start new terminal session 
		ANSIBLE_COLLECTIONS_PATHS=<path-to-collections-folders>
	
	3) Add below line in /etc/ansible/ansible.cfg File 
		
		collections_paths=<path-to-collection1>:<path-to-collection2>

	4) Keep your playbooks to run in relative to collection like in below example 

			|── myplaybook.yml
			├── collections/
			│   └── ansible_collections/
			│               └── a10/
			│                   └── acos_collection/<collection structure lives here>

C] Inside Playbook how to access Collection Modules : 
	
	1) You can use the FQCN (namespace.collection_name.module_name)  like below 
		
		tasks:
		 - a10.acos_collection.acos_command:
		 	- argument 
		 - a10.acos_collection.acos_config
		 	- argument 

	2) To avoid a lot of typing, you can use the collections keyword added in Ansible 2.8:
		
		collections:
		 - a10.acos_colllection

		tasks:
		 - acos_command:
		 	- argument 
		 - acos_config
		 	- argument 


