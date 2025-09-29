# Ansible Basics

This section covers the fundamental concepts of Ansible and how to use it to manage your homelab.

## Inventory Management

### Understanding the Inventory

The inventory file (`ansible/inventory/hosts`) defines your managed devices:

```ini
[raspberry_pis]
rpi1 ansible_host=192.168.1.10 ansible_user=pi

[desktop_computers]
desktop1 ansible_host=192.168.1.20 ansible_user=admin

[servers]
server1 ansible_host=192.168.1.30 ansible_user=admin

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

### Group Variables

Group variables are stored in `ansible/group_vars/`:

1. Create a file for each group:
   ```bash
   nano ansible/group_vars/raspberry_pis.yml
   ```

2. Add group-specific variables:
   ```yaml
   ---
   common_packages:
     - vim
     - htop
     - git
   ```

### Host Variables

Host-specific variables are stored in `ansible/host_vars/`:

1. Create a file for each host:
   ```bash
   nano ansible/host_vars/rpi1.yml
   ```

2. Add host-specific variables:
   ```yaml
   ---
   hostname: rpi1
   ip_address: 192.168.1.10
   ```

## Playbook Execution

### Running Playbooks

1. Run a specific playbook:
   ```bash
   ansible-playbook ansible/playbooks/site.yml
   ```

2. Run with specific tags:
   ```bash
   ansible-playbook ansible/playbooks/site.yml --tags "security,updates"
   ```

3. Run on specific hosts:
   ```bash
   ansible-playbook ansible/playbooks/site.yml --limit "raspberry_pis"
   ```

### Common Ansible Commands

1. Check host connectivity:
   ```bash
   ansible all -m ping
   ```

2. Run ad-hoc commands:
   ```bash
   ansible all -a "uptime"
   ```

3. Check facts about hosts:
   ```bash
   ansible all -m setup
   ```

## Writing Playbooks

### Basic Playbook Structure

```yaml
---
- name: Configure common settings
  hosts: all
  become: true
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
      when: ansible_os_family == "Debian"
```

### Using Roles

Roles help organize your playbooks:

1. Create a role:
   ```bash
   ansible-galaxy init ansible/roles/common
   ```

2. Use the role in a playbook:
   ```yaml
   ---
   - name: Apply common configuration
     hosts: all
     roles:
       - common
   ```

### Variables in Playbooks

Variables can be defined in multiple places:

1. In the playbook:
   ```yaml
   vars:
     admin_user: admin
   ```

2. In inventory files
3. In group_vars and host_vars
4. Using --extra-vars:
   ```bash
   ansible-playbook playbook.yml --extra-vars "admin_user=admin"
   ```

## Best Practices

1. **Use Roles**: Organize your playbooks into roles for better maintainability
2. **Version Control**: Keep your Ansible code in version control
3. **Documentation**: Document your playbooks and roles
4. **Testing**: Test playbooks in a staging environment first
5. **Idempotency**: Ensure your playbooks can be run multiple times safely

## Next Steps

Now that you understand the basics of Ansible, you can proceed to the [Security](security.md) section to learn about securing your homelab. 