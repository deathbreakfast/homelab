# Grafana Loki Stack Ansible Role

This role deploys a complete logging stack using Grafana Loki, Promtail, and Grafana for centralized log management across your homelab infrastructure.

## Components

### Grafana Loki
- **Purpose**: Log aggregation and storage
- **Port**: 3100
- **Features**: Efficient log storage, indexing, and querying
- **Resource Usage**: ~512MB RAM, 0.5 CPU cores

### Promtail
- **Purpose**: Log collection and shipping
- **Features**: Auto-discovery of Docker logs, system logs, and journal logs
- **Resource Usage**: ~256MB RAM, 0.25 CPU cores

### Grafana
- **Purpose**: Log visualization and dashboards
- **Port**: 3000
- **Features**: Beautiful dashboards, alerting, and log exploration
- **Resource Usage**: ~512MB RAM, 0.5 CPU cores

## Configuration

### Default Settings
- **Log Retention**: 31 days
- **Network**: Dedicated `logging` network
- **Data Directories**: `/opt/loki`, `/opt/grafana`
- **Admin User**: `admin`
- **Admin Password**: Set via `vault_grafana_admin_password`

### Customization
Override settings in your playbook or inventory:

```yaml
vars:
  loki_enabled: true
  promtail_enabled: true
  grafana_enabled: true
  loki_retention_period: "744h"  # 31 days
  grafana_admin_password: "your-secure-password"
```

## Deployment

### Option 1: Deploy with main playbook
```bash
cd /home/seanorourke/homelab/ansible
ansible-playbook -v playbooks/site.yml
```

### Option 2: Deploy logging stack separately
```bash
cd /home/seanorourke/homelab/ansible
ansible-playbook -v playbooks/logging.yml
```

## Usage

### Access Grafana
1. Navigate to `http://your-host:3000`
2. Login with admin credentials
3. Loki data source is automatically configured

### View Logs
1. Go to "Explore" in Grafana
2. Select "Loki" as data source
3. Use LogQL queries to search logs

### Example LogQL Queries
```
# All logs from Paperless containers
{job="docker"} |= "paperless"

# Error logs only
{job="docker"} |= "ERROR"

# System logs from specific host
{job="system"} |= "error"

# Docker container logs with specific labels
{container_name="paperless-webserver"}
```

## Features

### Automatic Log Collection
- **Docker Logs**: All container logs automatically collected
- **System Logs**: `/var/log/*.log` files monitored
- **Journal Logs**: Systemd journal logs collected
- **Custom Logs**: Configurable log directories

### Log Processing
- **Label Extraction**: Automatic labeling of log entries
- **Timestamp Parsing**: Proper timestamp handling
- **Log Parsing**: Structured log parsing with regex

### Visualization
- **Real-time Logs**: Live log streaming
- **Historical Data**: 31 days of log retention
- **Search & Filter**: Full-text search across all logs
- **Dashboards**: Pre-built and custom dashboards

## Resource Optimization

### Raspberry Pi Optimization
- **Memory Limits**: Configured for Pi 4B (4GB RAM)
- **CPU Limits**: Limited CPU usage
- **Storage**: Efficient compression and retention

### Multi-Device Setup
- **Centralized Loki**: One Loki instance per device
- **Distributed Promtail**: Promtail on each device
- **Single Grafana**: One Grafana instance for visualization

## Security

### Access Control
- **Admin Authentication**: Secure admin login
- **Network Isolation**: Dedicated logging network
- **File Permissions**: Proper file ownership and permissions

### Data Protection
- **Log Retention**: Automatic cleanup of old logs
- **Compression**: Efficient storage with compression
- **Encryption**: HTTPS support for Grafana

## Troubleshooting

### Common Issues

1. **Services Not Starting**
   ```bash
   # Check container status
   docker ps -a
   
   # Check logs
   docker logs loki
   docker logs promtail
   docker logs grafana
   ```

2. **No Logs Appearing**
   ```bash
   # Check Promtail configuration
   docker exec promtail cat /etc/promtail/config.yml
   
   # Check Loki connectivity
   curl http://localhost:3100/ready
   ```

3. **Grafana Connection Issues**
   ```bash
   # Check Grafana status
   curl http://localhost:3000/api/health
   
   # Check data source
   curl -u admin:password http://localhost:3000/api/datasources
   ```

### Logs
```bash
# View service logs
docker logs loki
docker logs promtail  
docker logs grafana

# Check configuration
cat /opt/loki/config/loki-config.yml
cat /opt/promtail/config/promtail-config.yml
cat /opt/grafana/config/grafana.ini
```

## Integration

This role integrates seamlessly with your existing homelab infrastructure:

- **Docker Integration**: Works with existing Docker containers
- **Ansible Integration**: Follows your existing Ansible patterns
- **Network Integration**: Uses dedicated logging network
- **Storage Integration**: Efficient storage management

## License

MIT

## Author Information

This role was created for homelab infrastructure management.
