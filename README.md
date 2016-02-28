# EECS 767 Term Project - Search Engine

This repository contains both the source code for the indexer and the web user interface used to search (aka "searcher"), as well as everything needed to bring up a development/demostration environment using Vagrant.

### Requirements
To get a development environment running "out of the box", the following dependencies are required (tested verions):

 - [Git] (v2.5.4)
 - [Virtual Box] (v5.0.14 r105127)
 - [Vagrant] (v1.8.1)
 - [Python] (v2.7.9)
 - [Ansible] (v1.9.2)

### Development Environment
If the above dependencies have been meet, then all that should be required to get a dev environment up and run is the following:

##### Step 1:
Pull down the latest version of the [project repository][git-repo-url] from Github ([git-repo-url]) into a prefered working directort on your local machine (`WORKING_DIR`).

##### Step 2:
From a terminal window execute the following commands:
 ```sh
  $ cd WORKING_DIR
  $ vagrant up
 ```
 You should see, in the output, Vagrant creating and configuring the VM ending with the Anisible "provisioning" playbook running.  The final line, before returning the prompt should look like:
 ```bash
PLAY RECAP ********************************************************************
default                    : ok=5    changed=4    unreachable=0    failed=0
 ```

If so, then you should be able to travel to [localhost:5000] in a browser, and if you see "Searching all the things!" then the dev environment is working correctly.

[Git]: https://git-scm.com
[Vagrant]: https://www.vagrantup.com
[Virtual Box]: https://www.virtualbox.org/wiki/Downloads
[Python]: https://www.python.org
[Ansible]: https://www.ansible.com/
[git-repo-url]: <https://github.com/wakewalker/eecs767.git>
[localhost:5000]: http://localhost:5000
