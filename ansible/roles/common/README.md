# Common Role

This role applies common configuration to all hosts in the infrastructure.

## Tasks

1. Updates the package manager cache (for Debian-based systems)
2. Installs common packages:
   - curl
   - wget
   - git
   - htop
   - vim
   - tmux
3. Creates an admin user (if defined)
4. Sets up SSH keys for the admin user (if defined)

## Variables

- `admin_user`: The username for the admin user (optional)
- `admin_ssh_key`: The SSH public key for the admin user (optional)

## Example Usage

```yaml
- hosts: all
  become: true
  vars:
    admin_user: admin
    admin_ssh_key: "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ..."
  roles:
    - common
``` 