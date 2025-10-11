#!/usr/bin/env python3
"""
Backup Exporter for Prometheus
Monitors local and cloud backups for Paperless-ngx
"""

import os
import json
import time
import subprocess
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackupExporter:
    def __init__(self, backup_dir: str = "/opt/backups/paperless", rclone_remote: str = "gdrive-crypt"):
        self.backup_dir = Path(backup_dir)
        self.rclone_remote = rclone_remote
        self.metrics = {}
        
    def get_local_backups(self) -> List[Dict]:
        """Get information about local backups"""
        backups = []
        
        if not self.backup_dir.exists():
            return backups
            
        for backup_path in self.backup_dir.glob("backup-*"):
            if backup_path.is_dir():
                try:
                    backup_name = backup_path.name
                    
                    # Extract timestamp from filename (format: backup-YYYYMMDD_HHMMSS)
                    backup_time = None
                    try:
                        # Parse the timestamp from the folder name
                        timestamp_str = backup_name.replace('backup-', '')
                        backup_time = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                        logger.debug(f"Extracted timestamp from filename {backup_name}: {backup_time}")
                    except ValueError as e:
                        logger.warning(f"Could not parse timestamp from filename {backup_name}: {e}")
                        # Fallback to modification time
                        mtime = backup_path.stat().st_mtime
                        backup_time = datetime.fromtimestamp(mtime)
                    
                    # Convert backup_time to Unix timestamp for Prometheus
                    backup_timestamp = int(backup_time.timestamp())
                    
                    # Map file names to backup types
                    file_type_map = {
                        'database.sql': 'Database',
                        'media.tar.gz': 'Media',
                        'data.tar.gz': 'Data',
                        'export.tar.gz': 'Export',
                        'static.tar.gz': 'Static'
                    }
                    
                    # Get individual file sizes
                    for file_name, backup_type in file_type_map.items():
                        file_path = backup_path / file_name
                        if file_path.exists() and file_path.is_file():
                            size_bytes = file_path.stat().st_size
                            backups.append({
                                'name': backup_name,
                                'type': backup_type,
                                'path': str(backup_path),
                                'size_bytes': size_bytes,
                                'backup_time': backup_time,
                                'backup_timestamp': backup_timestamp,
                                'age_hours': (datetime.now() - backup_time).total_seconds() / 3600,
                                'is_recent': (datetime.now() - backup_time).total_seconds() < 25 * 3600
                            })
                    
                    # Also add total backup size
                    total_size = sum(f.stat().st_size for f in backup_path.rglob('*') if f.is_file())
                    backups.append({
                        'name': backup_name,
                        'type': 'Total',
                        'path': str(backup_path),
                        'size_bytes': total_size,
                        'backup_time': backup_time,
                        'backup_timestamp': backup_timestamp,
                        'age_hours': (datetime.now() - backup_time).total_seconds() / 3600,
                        'is_recent': (datetime.now() - backup_time).total_seconds() < 25 * 3600
                    })
                    
                except Exception as e:
                    logger.error(f"Error processing backup {backup_path}: {e}")
                    
        return sorted(backups, key=lambda x: (x['backup_time'], x['type']), reverse=True)
    
    def get_cloud_backups(self) -> List[Dict]:
        """Get information about cloud backups from registry file"""
        backups = []
        
        try:
            # Read cloud backup registry file created by backup script
            registry_file = self.backup_dir / "cloud_backup_registry.json"
            
            if not registry_file.exists():
                logger.info("Cloud backup registry file not found, no cloud backups to report")
                return backups
            
            with open(registry_file, 'r') as f:
                registry_data = json.load(f)
            
            for entry in registry_data:
                backup_name = entry['name']
                size_bytes = entry['size_bytes']
                timestamp = entry['timestamp']
                
                # Convert timestamp to datetime
                backup_time = datetime.fromtimestamp(timestamp)
                
                # Calculate age
                age_hours = (datetime.now() - backup_time).total_seconds() / 3600
                is_recent = age_hours < 25  # Within 25 hours
                
                backups.append({
                    'name': backup_name,
                    'size_bytes': size_bytes,
                    'backup_time': backup_time,
                    'backup_timestamp': timestamp,
                    'age_hours': age_hours,
                    'is_recent': is_recent
                })
                
            logger.info(f"Loaded {len(backups)} cloud backups from registry")
            
        except Exception as e:
            logger.error(f"Error reading cloud backup registry: {e}")
        
        return sorted(backups, key=lambda x: x.get('backup_time', datetime.now()), reverse=True)
    
    def generate_metrics(self) -> str:
        """Generate Prometheus metrics"""
        metrics = []
        
        # Get backup data
        local_backups = self.get_local_backups()
        cloud_backups = self.get_cloud_backups()
        
        # Local backup metrics
        metrics.append("# HELP backup_local_count Number of local backups")
        metrics.append("# TYPE backup_local_count gauge")
        metrics.append(f"backup_local_count {len(local_backups)}")
        
        metrics.append("# HELP backup_local_total_size_bytes Total size of all local backups in bytes")
        metrics.append("# TYPE backup_local_total_size_bytes gauge")
        total_local_size = sum(b['size_bytes'] for b in local_backups)
        metrics.append(f"backup_local_total_size_bytes {total_local_size}")
        
        # Individual local backup metrics
        for backup in local_backups:
            backup_name = backup['name'].replace('-', '_').replace(':', '_')
            backup_type = backup['type']
            metrics.append(f"backup_local_size_bytes{{name=\"{backup['name']}\",type=\"{backup_type}\"}} {backup['size_bytes']}")
            metrics.append(f"backup_local_age_hours{{name=\"{backup['name']}\",type=\"{backup_type}\"}} {backup['age_hours']}")
            metrics.append(f"backup_local_timestamp{{name=\"{backup['name']}\",type=\"{backup_type}\"}} {backup['backup_timestamp']}")
            metrics.append(f"backup_local_is_recent{{name=\"{backup['name']}\",type=\"{backup_type}\"}} {1 if backup['is_recent'] else 0}")
        
        # Cloud backup metrics
        metrics.append("# HELP backup_cloud_count Number of cloud backups")
        metrics.append("# TYPE backup_cloud_count gauge")
        metrics.append(f"backup_cloud_count {len(cloud_backups)}")
        
        metrics.append("# HELP backup_cloud_total_size_bytes Total size of all cloud backups in bytes")
        metrics.append("# TYPE backup_cloud_total_size_bytes gauge")
        total_cloud_size = sum(b['size_bytes'] for b in cloud_backups)
        metrics.append(f"backup_cloud_total_size_bytes {total_cloud_size}")
        
        # Individual cloud backup metrics
        for backup in cloud_backups:
            metrics.append(f"backup_cloud_size_bytes{{name=\"{backup['name']}\"}} {backup['size_bytes']}")
            metrics.append(f"backup_cloud_age_hours{{name=\"{backup['name']}\"}} {backup['age_hours']}")
            metrics.append(f"backup_cloud_timestamp{{name=\"{backup['name']}\"}} {backup['backup_timestamp']}")
            metrics.append(f"backup_cloud_is_recent{{name=\"{backup['name']}\"}} {1 if backup['is_recent'] else 0}")
        
        # Backup health metrics
        latest_local = local_backups[0] if local_backups else None
        latest_cloud = cloud_backups[0] if cloud_backups else None
        
        metrics.append("# HELP backup_latest_local_age_hours Age of latest local backup in hours")
        metrics.append("# TYPE backup_latest_local_age_hours gauge")
        if latest_local:
            metrics.append(f"backup_latest_local_age_hours {latest_local['age_hours']}")
        else:
            metrics.append("backup_latest_local_age_hours -1")
        
        metrics.append("# HELP backup_latest_cloud_age_hours Age of latest cloud backup in hours")
        metrics.append("# TYPE backup_latest_cloud_age_hours gauge")
        if latest_cloud:
            metrics.append(f"backup_latest_cloud_age_hours {latest_cloud['age_hours']}")
        else:
            metrics.append("backup_latest_cloud_age_hours -1")
        
        # Backup success indicators
        metrics.append("# HELP backup_local_success 1 if recent local backup exists, 0 otherwise")
        metrics.append("# TYPE backup_local_success gauge")
        metrics.append(f"backup_local_success {1 if latest_local and latest_local['is_recent'] else 0}")
        
        metrics.append("# HELP backup_cloud_success 1 if recent cloud backup exists, 0 otherwise")
        metrics.append("# TYPE backup_cloud_success gauge")
        metrics.append(f"backup_cloud_success {1 if latest_cloud and latest_cloud['is_recent'] else 0}")
        
        return '\n'.join(metrics)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Backup Exporter for Prometheus')
    parser.add_argument('--backup-dir', default='/opt/backups/paperless', help='Local backup directory')
    parser.add_argument('--rclone-remote', default='gdrive-crypt', help='Rclone remote name')
    parser.add_argument('--port', type=int, default=9116, help='Port to serve metrics on')
    
    args = parser.parse_args()
    
    from http.server import HTTPServer, BaseHTTPRequestHandler
    
    class MetricsHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/metrics':
                exporter = BackupExporter(args.backup_dir, args.rclone_remote)
                metrics = exporter.generate_metrics()
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(metrics.encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
    
    server = HTTPServer(('0.0.0.0', args.port), MetricsHandler)
    logger.info(f"Starting backup exporter on port {args.port}")
    server.serve_forever()



