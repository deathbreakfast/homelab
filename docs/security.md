# Security

This section covers security best practices for your homelab, including Ansible Vault usage and SSH security.

## Ansible Vault

### Creating Encrypted Files

1. Create an encrypted variables file:
   ```bash
   ansible-vault create ansible/group_vars/all/vault.yml
   ```

2. Add sensitive variables:
   ```yaml
   ---
   admin_password: "secure_password"
   api_key: "your_api_key"
   ```

### Using Encrypted Files

1. Run playbooks with vault:
   ```bash
   ansible-playbook site.yml --ask-vault-pass
   ```

2. Or use a vault password file:
   ```bash
   ansible-playbook site.yml --vault-password-file ~/.vault_pass
   ```

### Managing Vault Files

1. Edit an encrypted file:
   ```bash
   ansible-vault edit ansible/group_vars/all/vault.yml
   ```

2. View an encrypted file:
   ```bash
   ansible-vault view ansible/group_vars/all/vault.yml
   ```

3. Change vault password:
   ```bash
   ansible-vault rekey ansible/group_vars/all/vault.yml
   ```

## SSH Security

### SSH Key Management

1. Generate strong SSH keys:
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```

2. Use a passphrase for your SSH key
3. Regularly rotate SSH keys
4. Remove old or unused keys from devices

### SSH Configuration

1. Secure SSH configuration on managed hosts:
   ```yaml
   - name: Configure SSH
     template:
       src: templates/sshd_config.j2
       dest: /etc/ssh/sshd_config
       owner: root
       group: root
       mode: '0644'
     notify: restart sshd
   ```

2. Example secure SSH configuration:
   ```ini
   PermitRootLogin no
   PasswordAuthentication no
   ChallengeResponseAuthentication no
   UsePAM yes
   X11Forwarding no
   AllowUsers admin
   ```

## Firewall Configuration

### Basic Firewall Setup

1. Install and configure UFW:
   ```yaml
   - name: Install UFW
     apt:
       name: ufw
       state: present

   - name: Configure UFW
     ufw:
       rule: allow
       port: '22'
       proto: tcp
     notify: restart ufw
   ```

2. Allow only necessary ports:
   ```yaml
   - name: Allow SSH
     ufw:
       rule: allow
       port: '22'
       proto: tcp

   - name: Allow HTTP
     ufw:
       rule: allow
       port: '80'
       proto: tcp
   ```

## Regular Updates

### System Updates

1. Configure automatic security updates:
   ```yaml
   - name: Install unattended-upgrades
     apt:
       name: unattended-upgrades
       state: present

   - name: Configure automatic updates
     template:
       src: templates/50unattended-upgrades.j2
       dest: /etc/apt/apt.conf.d/50unattended-upgrades
   ```

### Package Updates

1. Regular package updates:
   ```yaml
   - name: Update all packages
     apt:
       upgrade: dist
       update_cache: yes
     when: ansible_os_family == "Debian"
   ```

## Monitoring and Logging

### System Logging

1. Configure centralized logging:
   ```yaml
   - name: Install rsyslog
     apt:
       name: rsyslog
       state: present

   - name: Configure rsyslog
     template:
       src: templates/rsyslog.conf.j2
       dest: /etc/rsyslog.conf
   ```

### Security Monitoring

1. Install and configure fail2ban:
   ```yaml
   - name: Install fail2ban
     apt:
       name: fail2ban
       state: present

   - name: Configure fail2ban
     template:
       src: templates/jail.local.j2
       dest: /etc/fail2ban/jail.local
   ```

## Next Steps

Now that you understand the security aspects of your homelab, you can proceed to the [Troubleshooting](troubleshooting.md) section to learn how to handle common issues. 