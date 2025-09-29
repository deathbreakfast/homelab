# Troubleshooting

This section covers common issues you might encounter while managing your homelab and how to resolve them.

## Common Issues

### SSH Connection Problems

1. **Connection Refused**
   - Check if SSH service is running:
     ```bash
     systemctl status ssh
     ```
   - Verify firewall settings
   - Check if the port is correct in inventory

2. **Permission Denied**
   - Verify SSH key is properly copied:
     ```bash
     ssh-copy-id user@host
     ```
   - Check file permissions:
     ```bash
     chmod 700 ~/.ssh
     chmod 600 ~/.ssh/authorized_keys
     ```

### Ansible Connection Issues

1. **Python Interpreter Not Found**
   - Add to inventory:
     ```ini
     [all:vars]
     ansible_python_interpreter=/usr/bin/python3
     ```

2. **Host Unreachable**
   - Check network connectivity
   - Verify host is in inventory
   - Test SSH connection manually

### Playbook Execution Errors

1. **Permission Errors**
   - Add `become: true` to playbook
   - Verify sudo privileges
   - Check user permissions

2. **Package Installation Failures**
   - Update package lists:
     ```bash
     ansible all -m apt -a "update_cache=yes"
     ```
   - Check internet connectivity
   - Verify repository configuration

## Debugging Tips

### Verbose Output

1. Run playbook with verbose output:
   ```bash
   ansible-playbook playbook.yml -vvv
   ```

2. Check specific task:
   ```bash
   ansible-playbook playbook.yml --tags "specific-task" -vvv
   ```

### Gathering Facts

1. Check system facts:
   ```bash
   ansible all -m setup
   ```

2. Check specific fact:
   ```bash
   ansible all -m setup -a "filter=ansible_distribution*"
   ```

### Testing Connectivity

1. Test SSH connection:
   ```bash
   ansible all -m ping
   ```

2. Test specific host:
   ```bash
   ansible specific-host -m ping
   ```

## Ansible Vault Issues

1. **Vault Password Problems**
   - Verify vault password file permissions
   - Check vault password file content
   - Try running with `--ask-vault-pass`

2. **Encrypted File Access**
   - Verify file encryption:
     ```bash
     ansible-vault view file.yml
     ```
   - Check file permissions
   - Verify vault password is correct

## Network Troubleshooting

1. **DNS Resolution**
   - Check DNS configuration
   - Verify hosts file
   - Test DNS resolution:
     ```bash
     ansible all -m shell -a "nslookup example.com"
     ```

2. **Firewall Issues**
   - Check UFW status:
     ```bash
     ansible all -m shell -a "ufw status"
     ```
   - Verify port access
   - Check firewall rules

## Performance Issues

1. **Slow Playbook Execution**
   - Enable pipelining in ansible.cfg
   - Use `--forks` to increase parallelism
   - Optimize playbook structure

2. **High Resource Usage**
   - Monitor system resources
   - Check for resource-intensive tasks
   - Optimize playbook execution

## Getting Help

1. **Documentation**
   - Check Ansible documentation
   - Review playbook examples
   - Search online forums

2. **Community Support**
   - Ask on Ansible forums
   - Check GitHub issues
   - Join Ansible community

## Next Steps

After resolving any issues, you can:
1. Review your playbooks for potential improvements
2. Update your documentation
3. Consider implementing monitoring
4. Plan for future expansion 