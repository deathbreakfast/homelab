# Paperless-ngx Backup Role

This role sets up automated, encrypted backups for Paperless-ngx using rclone and cloud storage.

## Features

- **Automated backups** with cron scheduling
- **Complete data backup** including Docker volumes and PostgreSQL database
- **Encrypted cloud storage** using rclone crypt
- **Backup verification** with checksums
- **Automated restore functionality** with safety checks
- **Local restore support** for immediate recovery
- **Log rotation** and retention management
- **Multiple cloud providers** supported via rclone

## Requirements

- Paperless-ngx running in Docker
- rclone role installed
- Cloud storage account (Google Drive, AWS S3, Dropbox, etc.)
- Ansible 2.9 or later

## Configuration

### 1. Cloud Storage Setup

Configure your cloud storage in `group_vars/raspberry_pis.yml`:

```yaml
rclone_remotes:
  - name: "gdrive"
    type: "drive"
    client_id: "your_google_drive_client_id"
    client_secret: "your_google_drive_client_secret"
  - name: "gdrive-crypt"
    type: "crypt"
    remote: "gdrive:paperless-backup"
    password: "{{ vault_rclone_crypt_password }}"
    password2: "{{ vault_rclone_crypt_salt }}"
```

### 2. Backup Settings

```yaml
backup_base_dir: "/opt/backups/paperless"
backup_cron_hour: "2"  # Daily at 2 AM
backup_retention_days: 30
rclone_remote: "gdrive-crypt"
rclone_backup_path: "paperless-backup"
```

### 3. Security (Ansible Vault)

Create encrypted variables:

```bash
ansible-vault create group_vars/raspberry_pis_vault.yml
```

Add:
```yaml
vault_rclone_crypt_password: "your_strong_encryption_password"
vault_rclone_crypt_salt: "your_encryption_salt"
```

## Usage

### Deploy Backup System

```bash
ansible-playbook -i ansible/inventory/hosts ansible/playbooks/backup.yml
```

### Manual Operations

**Run backup manually:**
```bash
sudo -u pi /opt/backups/paperless/scripts/backup_paperless.sh
```

**Verify backups:**
```bash
sudo -u pi /opt/backups/paperless/scripts/verify_backup.sh
```

**Restore from backup (manual script):**
```bash
sudo -u pi /opt/backups/paperless/scripts/restore_paperless.sh backup-20240101_020000
```

**Restore from backup (Ansible playbook - cloud):**
```bash
ansible-playbook -e 'restore_backup_name=backup-20240101_020000' playbooks/restore_paperless.yml
```

**Restore from local backup (Ansible playbook - local):**
```bash
ansible-playbook -e 'restore_backup_path=/opt/backups/paperless/backup-20240101_020000' playbooks/restore_paperless_local.yml
```

**List available backups:**
```bash
rclone lsf gdrive-crypt:paperless-backup/
```

## What's Backed Up

The backup system creates a complete backup of your Paperless-ngx installation including:

### Docker Volumes
- **data.tar.gz** - Paperless data directory (classification models, etc.)
- **media.tar.gz** - Document files (originals, thumbnails, archives)
- **export.tar.gz** - Export directory
- **static.tar.gz** - Static files

### Database
- **database.sql** - Complete PostgreSQL database dump including:
  - User accounts and authentication
  - Document metadata (tags, correspondents, document types)
  - Processing rules and custom fields
  - Document relationships and history

### Metadata
- **backup-info.txt** - Backup metadata (date, system info, etc.)
- **checksums.txt** - SHA-256 checksums for integrity verification

## Backup Process

1. **Export Docker volumes** to compressed tarballs
2. **Backup PostgreSQL database** to SQL dump
3. **Create metadata** with backup information
4. **Generate checksums** for integrity verification
5. **Upload to encrypted cloud storage**
6. **Verify upload** with integrity check
7. **Clean up** old local backups

## Restore Process

1. **Download backup** from cloud storage (or use local backup)
2. **Verify integrity** with checksums
3. **Stop Paperless services**
4. **Create safety backup** of current data
5. **Extract and restore** Docker volumes
6. **Start database** service
7. **Restore database** from SQL dump
8. **Start all services** and verify
9. **Restart paperless-gpt** if present

## Security Features

- **End-to-end encryption** using rclone crypt
- **Checksum verification** for data integrity
- **Safe restore** with current data backup
- **Secure file permissions** (600 for config, 755 for scripts)
- **Log rotation** with retention policies

## Monitoring

- **Log files** in `/opt/backups/paperless/logs/`
- **Cron job** logs in system log
- **Backup verification** reports
- **Email notifications** (optional)

## Troubleshooting

### Common Issues

1. **Permission denied**: Ensure pi user has sudo access
2. **Cloud storage auth**: Run `rclone config` to set up authentication
3. **Backup fails**: Check logs in `/opt/backups/paperless/logs/`
4. **Restore issues**: Verify backup integrity first

### Logs

```bash
# View backup logs
tail -f /opt/backups/paperless/logs/backup-*.log

# Check cron job status
sudo systemctl status cron

# Verify rclone configuration
rclone config show
```

## License

MIT

## Author Information

This role was created for homelab infrastructure management.



