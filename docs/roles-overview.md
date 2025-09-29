# Ansible Roles Overview

This document provides detailed information about all Ansible roles in the homelab infrastructure.

## Infrastructure Roles

### `common`
**Purpose**: Applies common configuration to all hosts in the infrastructure.

**Key Features**:
- Updates package manager cache (Debian-based systems)
- Installs common packages: curl, wget, git, htop, vim, tmux
- Creates admin user (if defined)
- Sets up SSH keys for admin user (if defined)

**Dependencies**: None

**Variables**:
- `admin_user`: Username for admin user (optional)
- `admin_ssh_key`: SSH public key for admin user (optional)

**Usage**:
```yaml
- hosts: all
  become: true
  vars:
    admin_user: admin
    admin_ssh_key: "ssh-rsa AAAAB3NzaC1yc2E..."
  roles:
    - common
```

### `docker`
**Purpose**: Installs and configures Docker and Docker Compose.

**Key Features**:
- Installs Docker CE
- Installs Docker Compose
- Configures Docker daemon
- Adds user to docker group
- Enables Docker service

**Dependencies**: None

**Variables**:
- `docker_version`: Docker version to install
- `docker_compose_version`: Docker Compose version to install

### `server`
**Purpose**: Server-specific configuration and optimization.

**Key Features**:
- Server-specific package installation
- Performance tuning
- Security hardening
- Service configuration

**Dependencies**: `common`

### `desktop`
**Purpose**: Desktop computer specific configuration.

**Key Features**:
- Desktop environment setup
- GUI application installation
- Desktop-specific optimizations

**Dependencies**: `common`

### `raspberry_pi`
**Purpose**: Raspberry Pi specific configuration and optimization.

**Key Features**:
- Pi-specific package installation
- GPIO configuration
- Performance tuning for ARM architecture
- Power management

**Dependencies**: `common`

## Application Roles

### `paperless_ngx`
**Purpose**: Deploys Paperless-ngx document management system.

**Key Features**:
- Creates Paperless data directories
- Generates docker-compose.yml for Paperless stack
- Configures environment variables
- Starts Paperless services (web, db, redis, webserver)
- Waits for services to be ready

**Dependencies**: `docker`

**Variables**:
- `paperless_data_dir`: Directory for Paperless data
- `paperless_port`: Port for Paperless web interface
- `paperless_superuser_name`: Admin username
- `paperless_superuser_email`: Admin email
- `paperless_secret_key`: Django secret key
- `paperless_db_password`: Database password
- `paperless_superuser_password`: Admin password

**Services Deployed**:
- Paperless web application
- PostgreSQL database
- Redis cache
- Nginx reverse proxy

### `paperless_gpt`
**Purpose**: Adds AI-powered features to Paperless using OpenAI GPT.

**Key Features**:
- Integrates with existing Paperless installation
- Backs up original docker-compose.yml
- Updates docker-compose.yml to include Paperless-GPT
- Configures OpenAI API integration
- Sets up OCR and LLM processing
- Creates local PDF and HOCR directories (optional)

**Dependencies**: `docker`, `paperless_ngx`

**Variables**:
- `paperless_gpt_llm_provider`: LLM provider (openai, local, etc.)
- `paperless_gpt_llm_model`: LLM model to use
- `paperless_gpt_ocr_provider`: OCR provider
- `paperless_gpt_ocr_model`: OCR model
- `paperless_gpt_auto_process`: Enable automatic processing
- `paperless_gpt_enhanced_pdf`: Enable enhanced PDF features
- `paperless_gpt_port`: Port for Paperless-GPT interface

**Services Added**:
- Paperless-GPT service
- Enhanced document processing
- AI-powered OCR and classification

### `paperless_backup`
**Purpose**: Handles backup operations for Paperless data.

**Key Features**:
- Database backup
- Media files backup
- Configuration backup
- Automated backup scheduling
- Backup verification

**Dependencies**: `paperless_ngx`

### `rclone`
**Purpose**: Configures Rclone for cloud storage integration.

**Key Features**:
- Rclone installation
- Cloud provider configuration
- Sync operations setup
- Backup to cloud storage

**Dependencies**: None

## Monitoring & Logging Roles

### `prometheus_monitoring`
**Purpose**: Sets up comprehensive monitoring stack with Prometheus, Alertmanager, and Grafana.

**Key Features**:
- Prometheus metrics collection
- Alertmanager for alerting
- Grafana for visualization
- Docker network creation
- Service health checks
- Data source configuration

**Dependencies**: `docker`

**Variables**:
- `prometheus_enabled`: Enable Prometheus
- `alertmanager_enabled`: Enable Alertmanager
- `grafana_monitoring_enabled`: Enable Grafana
- `prometheus_port`: Prometheus port
- `alertmanager_port`: Alertmanager port
- `grafana_monitoring_port`: Grafana port

**Services Deployed**:
- Prometheus server
- Alertmanager
- Grafana monitoring instance
- Node exporter (for system metrics)

### `grafana_loki`
**Purpose**: Configures Grafana Loki for log aggregation and analysis.

**Key Features**:
- Loki log aggregation
- Log shipping configuration
- Log retention policies
- Integration with Grafana

**Dependencies**: `docker`

## Role Dependencies

```
common
├── server
├── desktop
├── raspberry_pi
└── docker
    ├── paperless_ngx
    │   ├── paperless_gpt
    │   └── paperless_backup
    ├── prometheus_monitoring
    └── grafana_loki

rclone (standalone)
```

## Role Execution Order

1. **Infrastructure**: `common` → `docker` → `server`/`desktop`/`raspberry_pi`
2. **Applications**: `paperless_ngx` → `paperless_gpt` → `paperless_backup`
3. **Monitoring**: `prometheus_monitoring` → `grafana_loki`
4. **Storage**: `rclone` (independent)

## Best Practices

1. **Role Dependencies**: Always ensure dependencies are met before running roles
2. **Variable Configuration**: Use Ansible Vault for sensitive variables
3. **Testing**: Test roles individually before combining in playbooks
4. **Documentation**: Keep role documentation updated with changes
5. **Idempotency**: Ensure roles can be run multiple times safely

## Troubleshooting

### Common Issues

1. **Docker Permission Errors**: Ensure user is in docker group
2. **Port Conflicts**: Check for existing services on required ports
3. **Disk Space**: Monitor disk usage for data directories
4. **Network Issues**: Verify Docker networks are created properly

### Debugging Commands

```bash
# Check role execution
ansible-playbook playbook.yml --check --diff

# Run specific role
ansible-playbook playbook.yml --tags "paperless_ngx"

# Debug mode
ansible-playbook playbook.yml -vvv
```
