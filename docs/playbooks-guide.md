# Ansible Playbooks Guide

This document provides comprehensive information about all Ansible playbooks in the homelab infrastructure.

## Main Orchestration Playbooks

### `site.yml`
**Purpose**: Main orchestration playbook that applies all configurations across the infrastructure.

**Structure**:
```yaml
- name: Apply common configuration to all hosts
  hosts: all
  roles:
    - common
    - grafana_loki
    - prometheus_monitoring

- name: Configure Raspberry Pi specific settings
  hosts: raspberry_pis
  roles:
    - raspberry_pi
    - docker
    - rclone
    - paperless_ngx
    - paperless_backup

- name: Configure desktop computers
  hosts: desktop_computers
  roles:
    - desktop

- name: Configure servers
  hosts: servers
  roles:
    - server
```

**Usage**:
```bash
# Run complete infrastructure setup
ansible-playbook ansible/playbooks/site.yml

# Run on specific host groups
ansible-playbook ansible/playbooks/site.yml --limit "raspberry_pis"

# Run with specific tags
ansible-playbook ansible/playbooks/site.yml --tags "docker,paperless"
```

## Application Deployment Playbooks

### `paperless.yml`
**Purpose**: Deploys complete Paperless-ngx stack with GPT integration on Raspberry Pi.

**Key Features**:
- Deploys Paperless-ngx document management
- Integrates Paperless-GPT for AI features
- Configures OpenAI API integration
- Sets up OCR and LLM processing
- Waits for services to be ready
- Displays access information

**Variables**:
```yaml
paperless_data_dir: "/opt/paperless"
paperless_port: 8000
paperless_superuser_name: "admin"
paperless_superuser_email: "admin@example.com"
paperless_secret_key: "changeme_secret_key_change_this"
paperless_db_password: "changeme_db_password_change_this"
paperless_superuser_password: "changeme_admin_password_change_this"

# Paperless-GPT configuration
paperless_gpt_llm_provider: "openai"
paperless_gpt_llm_model: "gpt-4o"
paperless_gpt_ocr_provider: "openai"
paperless_gpt_ocr_model: "gpt-4o"
paperless_gpt_auto_process: false
paperless_gpt_enhanced_pdf: true
```

**Usage**:
```bash
# Deploy Paperless with GPT
ansible-playbook ansible/playbooks/paperless.yml

# Deploy to specific Raspberry Pi
ansible-playbook ansible/playbooks/paperless.yml --limit "rpi1"
```

### `paperless-gpt.yml`
**Purpose**: Dedicated Paperless-GPT deployment (adds AI features to existing Paperless).

**Key Features**:
- Adds GPT capabilities to existing Paperless installation
- Configures OpenAI integration
- Updates docker-compose.yml
- Starts Paperless-GPT service

**Usage**:
```bash
# Add GPT to existing Paperless
ansible-playbook ansible/playbooks/paperless-gpt.yml
```

### `houselights.yml`
**Purpose**: Deploys the houselights Flask controller onto the `houselights` Raspberry Pi and ensures the service stays running.

**Key Features**:
- Installs required Python tooling and Git
- Clones `deathbreakfast/house-lights` into `/opt/houselights`
- Creates and manages a dedicated Python virtualenv
- Templates environment variables from host vars (LED count, GPIO pin, port)
- Registers and starts a `systemd` service (`houselights.service`)

**Usage**:
```bash
# First-time deployment / ensure service healthy
ansible-playbook ansible/playbooks/houselights.yml

# Limit to the houselights node explicitly (optional)
ansible-playbook ansible/playbooks/houselights.yml --limit "houselights"
```

### `houselights-update.yml`
**Purpose**: Pulls the latest code from GitHub, refreshes dependencies, and restarts the houselights service without re-running base package setup.

**Usage**:
```bash
# Update houselights application to the latest commit on the configured branch
ansible-playbook ansible/playbooks/houselights-update.yml
```

## Monitoring & Logging Playbooks

### `monitoring.yml`
**Purpose**: Deploys comprehensive monitoring stack.

**Structure**:
```yaml
- name: Deploy comprehensive monitoring stack
  hosts: rpi4b-01
  roles:
    - prometheus_monitoring

- name: Configure monitoring on Raspberry Pis
  hosts: rpi4b-01
  roles:
    - prometheus_monitoring

- name: Configure monitoring on desktop computers
  hosts: desktops
  roles:
    - prometheus_monitoring

- name: Configure monitoring on servers
  hosts: servers
  roles:
    - prometheus_monitoring
```

**Services Deployed**:
- Prometheus (metrics collection)
- Alertmanager (alerting)
- Grafana (visualization)
- Node Exporter (system metrics)

**Usage**:
```bash
# Deploy monitoring stack
ansible-playbook ansible/playbooks/monitoring.yml

# Deploy to specific hosts
ansible-playbook ansible/playbooks/monitoring.yml --limit "servers"
```

### `logging.yml`
**Purpose**: Sets up centralized logging infrastructure.

**Key Features**:
- Grafana Loki log aggregation
- Log shipping configuration
- Log retention policies
- Integration with monitoring stack

**Usage**:
```bash
# Deploy logging infrastructure
ansible-playbook ansible/playbooks/logging.yml
```

## Backup & Restore Playbooks

### `backup.yml`
**Purpose**: Comprehensive backup operations for the homelab infrastructure.

**Key Features**:
- Database backups
- Configuration backups
- Media file backups
- Cloud storage integration
- Backup verification

**Usage**:
```bash
# Run full backup
ansible-playbook ansible/playbooks/backup.yml

# Backup specific services
ansible-playbook ansible/playbooks/backup.yml --tags "paperless"
```

### `restore_paperless.yml`
**Purpose**: Restore Paperless from backup.

**Key Features**:
- Database restoration
- Media file restoration
- Configuration restoration
- Service restart

**Usage**:
```bash
# Restore Paperless from backup
ansible-playbook ansible/playbooks/restore_paperless.yml

# Restore from specific backup
ansible-playbook ansible/playbooks/restore_paperless.yml --extra-vars "backup_date=2024-01-15"
```

### `restore_paperless_local.yml`
**Purpose**: Local restore operations for Paperless.

**Key Features**:
- Local backup restoration
- File system restoration
- Service configuration

**Usage**:
```bash
# Restore from local backup
ansible-playbook ansible/playbooks/restore_paperless_local.yml
```

### `trigger_backup.yml`
**Purpose**: Trigger backup processes manually.

**Key Features**:
- Manual backup initiation
- Scheduled backup execution
- Backup status monitoring

**Usage**:
```bash
# Trigger backup
ansible-playbook ansible/playbooks/trigger_backup.yml

# Trigger specific backup type
ansible-playbook ansible/playbooks/trigger_backup.yml --extra-vars "backup_type=full"
```

### `trigger_restore.yml`
**Purpose**: Trigger restore processes.

**Key Features**:
- Manual restore initiation
- Restore verification
- Service restart after restore

**Usage**:
```bash
# Trigger restore
ansible-playbook ansible/playbooks/trigger_restore.yml
```

### `verify_backup.yml`
**Purpose**: Verify backup integrity and completeness.

**Key Features**:
- Backup file verification
- Checksum validation
- Backup completeness check
- Restore test (optional)

**Usage**:
```bash
# Verify all backups
ansible-playbook ansible/playbooks/verify_backup.yml

# Verify specific backup
ansible-playbook ansible/playbooks/verify_backup.yml --extra-vars "backup_date=2024-01-15"
```

## System Management Playbooks

### `update-system.yml`
**Purpose**: System updates and maintenance operations.

**Key Features**:
- Package updates
- Security patches
- Service restarts
- System optimization

**Usage**:
```bash
# Update all systems
ansible-playbook ansible/playbooks/update-system.yml

# Update specific hosts
ansible-playbook ansible/playbooks/update-system.yml --limit "raspberry_pis"
```

## Playbook Execution Best Practices

### 1. Dry Run Testing
```bash
# Test playbook without making changes
ansible-playbook playbook.yml --check --diff

# Test with verbose output
ansible-playbook playbook.yml --check --diff -vvv
```

### 2. Targeted Execution
```bash
# Run on specific hosts
ansible-playbook playbook.yml --limit "rpi1,desktop1"

# Run on specific host groups
ansible-playbook playbook.yml --limit "raspberry_pis"

# Skip specific hosts
ansible-playbook playbook.yml --limit "all:!servers"
```

### 3. Tag-based Execution
```bash
# Run specific tags
ansible-playbook playbook.yml --tags "docker,paperless"

# Skip specific tags
ansible-playbook playbook.yml --skip-tags "backup"
```

### 4. Variable Overrides
```bash
# Override variables
ansible-playbook playbook.yml --extra-vars "paperless_port=8080"

# Use variable files
ansible-playbook playbook.yml --extra-vars "@custom-vars.yml"
```

### 5. Parallel Execution
```bash
# Run with multiple forks
ansible-playbook playbook.yml --forks 10

# Limit concurrent operations
ansible-playbook playbook.yml --forks 5
```

## Troubleshooting

### Common Issues

1. **Connection Timeouts**:
   ```bash
   # Increase timeout
   ansible-playbook playbook.yml --timeout 60
   ```

2. **Permission Errors**:
   ```bash
   # Run with become
   ansible-playbook playbook.yml --become
   ```

3. **Variable Issues**:
   ```bash
   # Debug variables
   ansible-playbook playbook.yml --extra-vars "debug_vars=true"
   ```

### Debugging Commands

```bash
# Verbose output
ansible-playbook playbook.yml -vvv

# Check syntax
ansible-playbook playbook.yml --syntax-check

# List hosts
ansible-playbook playbook.yml --list-hosts

# List tags
ansible-playbook playbook.yml --list-tags
```

## Playbook Dependencies

```
site.yml (main orchestration)
├── paperless.yml
│   ├── paperless-gpt.yml
│   └── backup.yml
├── monitoring.yml
├── logging.yml
└── update-system.yml

Backup Operations:
├── backup.yml
├── trigger_backup.yml
├── verify_backup.yml
└── restore_paperless.yml
    └── restore_paperless_local.yml
```

## Security Considerations

1. **Use Ansible Vault** for sensitive variables
2. **Limit sudo access** to necessary operations
3. **Use SSH keys** instead of passwords
4. **Regular updates** of playbooks and roles
5. **Audit playbook execution** logs

## Performance Optimization

1. **Use tags** to run only necessary tasks
2. **Limit host groups** when possible
3. **Use parallel execution** for independent tasks
4. **Cache facts** when running multiple playbooks
5. **Optimize variable usage** to reduce memory usage
