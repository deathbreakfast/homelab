#!/bin/bash

# Install required Ansible collections for the logging stack
echo "Installing required Ansible collections..."

# Install collections
ansible-galaxy collection install community.docker
ansible-galaxy collection install community.general
ansible-galaxy collection install ansible.posix

echo "Collections installed successfully!"
echo "You can now run the logging playbook:"
echo "ansible-playbook -v playbooks/logging.yml"
