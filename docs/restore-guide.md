# Paperless-ngx Restore Guide

This guide explains how to restore your Paperless-ngx installation from backups using the automated Ansible playbooks.

## Prerequisites

- Ansible installed and configured
- Access to the homelab repository
- Backup files available (either locally or in cloud storage)

## Restore Options

### 1. Restore from Cloud Storage (Recommended)

Use this method when your backups are stored in cloud storage (Google Drive, AWS S3, etc.):

```bash
cd /home/seanorourke/homelab/ansible
ansible-playbook -e 'restore_backup_name=backup-20250929_020013' playbooks/restore_paperless.yml
```

**Parameters:**
- `restore_backup_name`: Name of the backup to restore (e.g., `backup-20250929_020013`)

### 2. Restore from Local Backup

Use this method when you have backup files locally on the Raspberry Pi:

```bash
cd /home/seanorourke/homelab/ansible
ansible-playbook -e 'restore_backup_path=/opt/backups/paperless/backup-20250929_020013' playbooks/restore_paperless_local.yml
```

**Parameters:**
- `restore_backup_path`: Full path to the backup directory

### 3. Force Restore (Skip Safety Checks)

If Paperless-ngx is running and you want to force the restore:

```bash
ansible-playbook -e 'restore_backup_name=backup-20250929_020013' -e 'restore_force=true' playbooks/restore_paperless.yml
```

## What Gets Restored

The restore process will restore:

### ✅ Complete Data Recovery
- **Document files** (PDFs, images, thumbnails)
- **Database** (users, tags, correspondents, document types, metadata)
- **Configuration** (processing rules, custom fields)
- **System data** (classification models, etc.)

### 🔄 Automatic Service Management
- Stops running Paperless-ngx services
- Creates safety backup of current data
- Restores all volumes and database
- Restarts all services
- Restarts paperless-gpt if present

## Before You Start

1. **List available backups** to see what's available:
   ```bash
   # For cloud backups
   rclone lsf gdrive-crypt:paperless-backup/
   
   # For local backups
   ls -la /opt/backups/paperless/backup-*
   ```

2. **Verify backup integrity** (optional but recommended):
   ```bash
   cd /opt/backups/paperless/backup-20250929_020013
   sha256sum -c checksums.txt
   ```

## During Restore

The playbook will:

1. **Validate** the backup exists and is accessible
2. **Check** if Paperless-ngx is running (will stop it safely)
3. **Create** a safety backup of current data
4. **Download** or copy backup files to temporary location
5. **Verify** backup integrity with checksums
6. **Stop** all Paperless-ngx services
7. **Extract** and restore Docker volumes
8. **Start** database service
9. **Restore** database from SQL dump
10. **Start** all services
11. **Restart** paperless-gpt if present
12. **Clean up** temporary files

## After Restore

1. **Verify access** to Paperless-ngx at `http://192.168.0.45:8000`
2. **Check** that your documents are visible
3. **Verify** tags, correspondents, and document types are restored
4. **Test** paperless-gpt at `http://192.168.0.45:8080` if deployed
5. **Recreate** any missing tags or document types if needed

## Troubleshooting

### Restore Fails with "Services Running" Error
```bash
# Force the restore
ansible-playbook -e 'restore_backup_name=backup-20250929_020013' -e 'restore_force=true' playbooks/restore_paperless.yml
```

### Backup Not Found
- Verify the backup name is correct
- Check if the backup exists in cloud storage or locally
- Ensure you have proper permissions to access the backup

### Database Restore Fails
- Check that the database container is running
- Verify database credentials in docker-compose.yml
- Check the database.sql file exists in the backup

### Services Don't Start After Restore
```bash
# Check service logs
ssh pi@192.168.0.45 "cd /opt/paperless && docker-compose logs"

# Restart services manually
ssh pi@192.168.0.45 "cd /opt/paperless && docker-compose down && docker-compose up -d"
```

## Safety Features

- **Automatic safety backup** of current data before restore
- **Integrity verification** with SHA-256 checksums
- **Service validation** to ensure everything is running
- **Rollback capability** using the safety backup if needed

## Recovery from Safety Backup

If something goes wrong, you can restore from the safety backup:

```bash
# The safety backup is automatically created at:
# /opt/backups/paperless/current-backup-YYYYMMDDTHHMMSS

ansible-playbook -e 'restore_backup_path=/opt/backups/paperless/current-backup-20250929_140000' playbooks/restore_paperless_local.yml
```

## Best Practices

1. **Test restores** regularly to ensure backups work
2. **Keep multiple backup versions** for redundancy
3. **Verify backups** before deleting old ones
4. **Document** any custom configurations
5. **Monitor** the restore process for any errors

---

For more information about the backup system, see [backup.md](backup.md).
