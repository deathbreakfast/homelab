# Docker Role

This role installs and configures Docker and Docker Compose on Debian/Ubuntu systems.

## Features

- Installs Docker and Docker Compose from system packages
- Starts and enables the Docker service
- Adds the specified user to the docker group
- Sets proper permissions on the Docker socket
- Tests Docker functionality

## Requirements

- Debian/Ubuntu system
- User with sudo privileges
- Ansible 2.9 or later

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `docker_user` | `{{ ansible_user }}` | User to add to docker group |
| `docker_group` | `docker` | Docker group name |
| `docker_service_enabled` | `true` | Whether to enable Docker service |
| `docker_service_state` | `started` | Docker service state |

## Dependencies

None.

## Example Playbook

```yaml
---
- hosts: servers
  become: true
  roles:
    - docker
```

## Example with Custom User

```yaml
---
- hosts: servers
  become: true
  vars:
    docker_user: "myuser"
  roles:
    - docker
```

## License

MIT

## Author Information

This role was created for homelab infrastructure management.



