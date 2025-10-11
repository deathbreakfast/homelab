#!/bin/bash

# Backup Metrics Script for Prometheus
# Creates metrics files that can be read by Node Exporter's textfile collector

BACKUP_DIR="/opt/backups/paperless"
METRICS_DIR="/var/lib/node_exporter/textfile_collector"
METRICS_FILE="$METRICS_DIR/backup_metrics.prom"

# Create metrics directory if it doesn't exist
mkdir -p "$METRICS_DIR"

# Function to get backup information
get_backup_info() {
    local backup_path="$1"
    local backup_name=$(basename "$backup_path")
    local backup_size=$(du -sb "$backup_path" 2>/dev/null | cut -f1)
    local backup_mtime=$(stat -c %Y "$backup_path" 2>/dev/null)
    local backup_age_hours=$(( ($(date +%s) - backup_mtime) / 3600 ))
    
    echo "backup_local_size_bytes{name=\"$backup_name\"} $backup_size"
    echo "backup_local_age_hours{name=\"$backup_name\"} $backup_age_hours"
    echo "backup_local_is_recent{name=\"$backup_name\"} $([ $backup_age_hours -lt 25 ] && echo 1 || echo 0)"
}

# Function to get cloud backup info (if rclone is available)
get_cloud_backup_info() {
    if command -v rclone >/dev/null 2>&1; then
        # This is a simplified version - you might need to adjust based on your rclone setup
        local cloud_backups=$(rclone ls gdrive-crypt:paperless-backup --json 2>/dev/null | jq -r 'select(.IsDir == true) | .Path' | wc -l)
        echo "backup_cloud_count $cloud_backups"
    else
        echo "backup_cloud_count 0"
    fi
}

# Create metrics file
{
    echo "# HELP backup_local_count Number of local backups"
    echo "# TYPE backup_local_count gauge"
    
    # Count local backups
    local backup_count=0
    if [ -d "$BACKUP_DIR" ]; then
        backup_count=$(find "$BACKUP_DIR" -name "backup-*" -type d | wc -l)
    fi
    echo "backup_local_count $backup_count"
    
    echo "# HELP backup_local_total_size_bytes Total size of all local backups in bytes"
    echo "# TYPE backup_local_total_size_bytes gauge"
    
    # Calculate total size
    local total_size=0
    if [ -d "$BACKUP_DIR" ]; then
        total_size=$(du -sb "$BACKUP_DIR" 2>/dev/null | cut -f1)
    fi
    echo "backup_local_total_size_bytes $total_size"
    
    echo "# HELP backup_local_size_bytes Size of individual local backups in bytes"
    echo "# TYPE backup_local_size_bytes gauge"
    echo "# HELP backup_local_age_hours Age of individual local backups in hours"
    echo "# TYPE backup_local_age_hours gauge"
    echo "# HELP backup_local_is_recent Whether backup is recent (within 25 hours)"
    echo "# TYPE backup_local_is_recent gauge"
    
    # Get individual backup info
    if [ -d "$BACKUP_DIR" ]; then
        find "$BACKUP_DIR" -name "backup-*" -type d | while read backup_path; do
            get_backup_info "$backup_path"
        done
    fi
    
    echo "# HELP backup_cloud_count Number of cloud backups"
    echo "# TYPE backup_cloud_count gauge"
    get_cloud_backup_info
    
    # Backup health indicators
    echo "# HELP backup_latest_local_age_hours Age of latest local backup in hours"
    echo "# TYPE backup_latest_local_age_hours gauge"
    
    local latest_age=-1
    if [ -d "$BACKUP_DIR" ]; then
        latest_backup=$(find "$BACKUP_DIR" -name "backup-*" -type d -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)
        if [ -n "$latest_backup" ]; then
            latest_mtime=$(stat -c %Y "$latest_backup" 2>/dev/null)
            latest_age=$(( ($(date +%s) - latest_mtime) / 3600 ))
        fi
    fi
    echo "backup_latest_local_age_hours $latest_age"
    
    echo "# HELP backup_local_success Whether recent local backup exists"
    echo "# TYPE backup_local_success gauge"
    local success=0
    if [ $latest_age -ge 0 ] && [ $latest_age -lt 25 ]; then
        success=1
    fi
    echo "backup_local_success $success"
    
} > "$METRICS_FILE"

# Set proper permissions
chmod 644 "$METRICS_FILE"







