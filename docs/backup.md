# Paperless-ngx Backup Guide

This guide explains how to configure the automated Paperless-ngx backup system and sync encrypted backups to cloud storage providers such as Google Drive or AWS S3 using rclone.

## Overview

The backup role provides:

- Encrypted backups using `rclone crypt`
- Automated scheduling with cron
- Helper scripts for backup, verification, and restore
- Support for any rclone-supported cloud provider
- Integrity checks using SHA-256 checksums
- Log rotation and retention controls

Backups are staged under `/opt/backups/paperless` before being uploaded to cloud storage.

## Inventory Configuration

The backup system uses a proper Ansible directory structure with group variables in the correct location.

### Directory Structure
```
ansible/
├── inventory/
│   ├── hosts
│   └── group_vars/
│       └── raspberry_pis/
│           ├── vars.yml          # Non-sensitive configuration
│           └── vault.yml          # Encrypted sensitive data
├── playbooks/
│   ├── backup.yml                 # Main backup setup
│   ├── trigger_backup.yml         # Manual backup trigger
│   ├── trigger_restore.yml        # Manual restore trigger
│   └── verify_backup.yml          # Backup verification
└── roles/
    ├── rclone/                    # rclone installation & config
    └── paperless_backup/          # Backup scripts & scheduling
```

### Group Variables Configuration

**File: `ansible/inventory/group_vars/raspberry_pis/vars.yml`** (Non-sensitive config):
```yaml
# Paperless-ngx configuration
paperless_data_dir: "/opt/paperless"
paperless_port: 8000
paperless_superuser_name: "admin"
paperless_superuser_email: "admin@example.com"
paperless_ocr_language: "eng"
paperless_timezone: "America/Los_Angeles"

# Docker configuration
docker_packages:
  - docker.io
  - docker-compose

# Rclone configuration
rclone_remotes:
  - name: "gdrive"
    type: "drive"
    client_id: "{{ vault_gdrive_client_id }}"
    client_secret: "{{ vault_gdrive_client_secret }}"
  - name: "gdrive-crypt"
    type: "crypt"
    remote: "gdrive:paperless-backup"
    password: "{{ vault_rclone_crypt_password }}"
    password2: "{{ vault_rclone_crypt_salt }}"

# Backup configuration
backup_base_dir: "/opt/backups/paperless"
backup_cron_hour: "2"
backup_cron_minute: "0"
backup_retention_days: 30
rclone_remote: "gdrive-crypt"
rclone_backup_path: "paperless-backup"
backup_verify_enabled: true
backup_verify_checksums: true
```

**File: `ansible/inventory/group_vars/raspberry_pis/vault.yml`** (Encrypted sensitive data):
```yaml
# Google Drive OAuth credentials
vault_gdrive_client_id: "your_google_client_id"
vault_gdrive_client_secret: "your_google_client_secret"
vault_gdrive_token: '{"access_token":"...","token_type":"Bearer","refresh_token":"...","expiry":"..."}'

# rclone crypt encryption (MUST be obscured passwords)
vault_rclone_crypt_password: "obscured_password_from_rclone_obscure"
vault_rclone_crypt_salt: "obscured_salt_from_rclone_obscure"

# Paperless security settings (override defaults)
vault_paperless_secret_key: "your_secret_key"
vault_paperless_db_password: "your_db_password"
vault_paperless_superuser_password: "your_admin_password"
```

> **Important:** The vault file must be encrypted with Ansible Vault:
```bash
ansible-vault create ansible/inventory/group_vars/raspberry_pis/vault.yml
```

## Generate Encryption Credentials

Before configuring the backup system, you need to generate strong encryption credentials for the crypt remote:

### Step 1: Generate Raw Encryption Credentials
```bash
# Generate the encryption password (32 bytes, base64 encoded)
openssl rand -base64 32

# Generate the salt (16 bytes, base64 encoded)  
openssl rand -base64 16
```

**Important:** Save these raw values securely in your password manager. If you lose them, you cannot decrypt your backups.

### Step 2: Obscure the Passwords for rclone
rclone requires obscured passwords in the configuration file. Use `rclone obscure` to convert your raw passwords:

```bash
# Obscure the password
rclone obscure "your_generated_password_here"

# Obscure the salt
rclone obscure "your_generated_salt_here"
```

### Step 3: Add Obscured Values to Vault
Add the **obscured** values (not the raw ones) to your vault file:
```yaml
vault_rclone_crypt_password: "obscured_password_from_rclone_obscure"
vault_rclone_crypt_salt: "obscured_salt_from_rclone_obscure"
```

> **Critical:** Use the obscured values in the vault file, not the raw base64 values. rclone expects obscured passwords in the configuration.

## Configure Google Drive Remote

### Step 1: Get Google Drive OAuth Credentials
1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create (or select) a project and enable the **Google Drive API**.
3. Under **APIs & Services → Credentials**, create OAuth 2.0 credentials (Desktop app).
4. Record the `client_id` and `client_secret` and store them in your vault file.

### Step 2: Generate OAuth Token
Generate a complete OAuth token on your laptop (with a browser):
```bash
rclone authorize "drive" --client-id "<your_client_id>" --client-secret "<your_client_secret>"
```

Copy the JSON output (looks like `{"access_token":"...","refresh_token":"...","expiry":"..."}`).

### Step 3: Add Credentials to Vault
Add your Google Drive credentials to `ansible/inventory/group_vars/raspberry_pis/vault.yml`:
```yaml
vault_gdrive_client_id: "your_google_client_id"
vault_gdrive_client_secret: "your_google_client_secret"
vault_gdrive_token: '{"access_token":"...","token_type":"Bearer","refresh_token":"...","expiry":"..."}'
```

**That's it!** The Ansible role will automatically:
- Configure the `gdrive` remote with your OAuth credentials
- Create the `gdrive-crypt` remote that wraps the Drive remote
- Set up the encrypted backup folder at `gdrive:paperless-backup`

References: [rclone drive docs](https://rclone.org/drive/) and [rclone crypt docs](https://rclone.org/crypt/).

## Configure AWS S3 Remote

1. Create an IAM user with programmatic access.
2. Attach a policy granting access to your backup bucket.
3. Create the S3 bucket (for example `paperless-backups`).
4. Store the AWS credentials in Ansible Vault.
5. Add the rclone remotes:

```yaml
rclone_remotes:
  - name: "s3"
    type: "s3"
    provider: "AWS"
    env_auth: "false"
    access_key_id: "{{ vault_aws_access_key }}"
    secret_access_key: "{{ vault_aws_secret_key }}"
    region: "us-east-1"
    location_constraint: "us-east-1"
    acl: "private"
  - name: "s3-crypt"
    type: "crypt"
    remote: "s3:paperless-backups"
    password: "{{ vault_rclone_crypt_password }}"
    password2: "{{ vault_rclone_crypt_salt }}"
```

Reference: [rclone s3 docs](https://rclone.org/s3/).

## Deploy the Backup System

### Prerequisites
1. Ensure you're in the `ansible/` directory (required for `ansible.cfg` to be loaded)
2. Verify your vault file is encrypted and contains obscured passwords
3. Confirm Google Drive OAuth credentials are valid

### Deploy the Backup System
```bash
cd ansible/
ansible-playbook playbooks/backup.yml
```

This will:
- Install and configure rclone with your cloud storage credentials
- Create backup directories and scripts
- Set up automated scheduling with cron
- Configure log rotation

### Verify the Setup
After deployment, verify the rclone configuration:
```bash
# Check that rclone config was created with obscured passwords
ansible raspberry_pis -m shell -a "cat /home/pi/.config/rclone/rclone.conf"
```

The main `site.yml` playbook already includes the `rclone` and `paperless_backup` roles for Raspberry Pis.

## Generated Scripts

Scripts are installed in `/opt/backups/paperless/scripts/`:

- `backup_paperless.sh`
- `verify_backup.sh`
- `restore_paperless.sh`
- `backup_notify.sh` (created when notifications are enabled)

Logs live in `/opt/backups/paperless/logs/` and are rotated via `/etc/logrotate.d/paperless-backup`.

## Scheduling

A cron job runs at the configured time (default: daily at 02:00). Adjust `backup_cron_hour` and `backup_cron_minute` as needed.

## Manual Backup Operations

### Trigger a Manual Backup
```bash
cd ansible/
ansible-playbook playbooks/trigger_backup.yml
```

### Verify Backup Integrity
```bash
cd ansible/
ansible-playbook playbooks/verify_backup.yml
```

### Restore from Backup
```bash
cd ansible/
ansible-playbook playbooks/trigger_restore.yml -e backup_to_restore=backup-YYYYMMDD_HHMMSS
```

Or run directly on the target machine:
```bash
sudo -u pi /opt/backups/paperless/scripts/restore_paperless.sh backup-YYYYMMDD_HHMMSS
```

Add `--force` to restore while Paperless is running (the script still creates a safety snapshot).

## Monitoring & Verification

- Review `/opt/backups/paperless/logs/` for run logs.
- Run `verify_backup.sh` periodically to confirm backup integrity.
- Check cron execution via `/var/log/syslog` or convert the cron job to a systemd timer if preferred.

## Security Considerations

- **Vault Files**: Keep encrypted; never commit secrets in plain text
- **Encryption Passwords**: Protect them—losing them renders backups unrecoverable
- **Cloud Access**: Restrict access to cloud buckets/folders used for backups
- **Credential Rotation**: Rotate OAuth credentials periodically and audit access
- **Password Format**: Always use `rclone obscure` for crypt passwords in vault files
- **Directory Structure**: Use proper Ansible group_vars structure for variable precedence

## Troubleshooting

### Common Issues

**"base64 decode failed when revealing password"**
- **Cause**: Using raw base64 passwords instead of obscured passwords
- **Fix**: Use `rclone obscure` to convert passwords and update vault file

**"didn't find section in config file"**
- **Cause**: rclone config not found in expected location
- **Fix**: Ensure config is in `/home/pi/.config/rclone/rclone.conf` and copied to `/root/.config/rclone/rclone.conf`

**"empty token found - please run rclone config reconnect"**
- **Cause**: Google Drive OAuth token expired or missing
- **Fix**: Run `rclone config reconnect gdrive:` or regenerate OAuth credentials

**"VARIABLE IS NOT DEFINED!"**
- **Cause**: Group variables not loading due to incorrect directory structure
- **Fix**: Ensure group_vars are in `inventory/group_vars/raspberry_pis/` directory

### Verification Commands
```bash
# Check rclone configuration
ansible raspberry_pis -m shell -a "cat /etc/rclone/rclone.conf"

# Test rclone connectivity
ansible raspberry_pis -m shell -a "RCLONE_CONFIG=/etc/rclone/rclone.conf rclone lsd gdrive:"

# Test encrypted remote connectivity
ansible raspberry_pis -m shell -a "RCLONE_CONFIG=/etc/rclone/rclone.conf rclone lsd gdrive-crypt:"

# Check backup script syntax
ansible raspberry_pis -m shell -a "bash -n /opt/backups/paperless/scripts/backup_paperless.sh"
```
