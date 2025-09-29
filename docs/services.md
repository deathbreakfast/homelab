# Services Documentation

This document provides detailed information about all services deployed in the homelab infrastructure.

## Document Management Services

### Paperless-ngx
**Purpose**: Open-source document management system for digitizing and organizing documents.

**Key Features**:
- Document upload and storage
- OCR (Optical Character Recognition) processing
- Automatic document classification
- Full-text search capabilities
- Tag and category management
- Export and sharing options
- REST API for integration

**Configuration**:
- **Port**: 8000
- **Database**: PostgreSQL
- **Cache**: Redis
- **Web Server**: Nginx
- **OCR Engine**: Tesseract

**Access**:
- Web Interface: `http://<host>:8000`
- API: `http://<host>:8000/api/`
- Admin Panel: `http://<host>:8000/admin/`

**Default Credentials**:
- Username: `admin`
- Email: `admin@example.com`
- Password: `changeme_admin_password_change_this`

**Important**: Change default passwords after first login!

### Paperless-GPT
**Purpose**: AI-powered enhancement for Paperless-ngx using OpenAI GPT models.

**Key Features**:
- AI-powered OCR using OpenAI Vision
- Intelligent document classification
- Content extraction and summarization
- Metadata enhancement
- Automated document processing
- Enhanced search capabilities

**Configuration**:
- **Port**: 8001
- **LLM Provider**: OpenAI
- **LLM Model**: GPT-4o
- **OCR Provider**: OpenAI Vision
- **Auto Process**: Disabled by default

**Access**:
- Web Interface: `http://<host>:8001`
- Health Check: `http://<host>:8001/health`

**Requirements**:
- OpenAI API key (configured in vault)
- Internet connection for API calls
- Sufficient compute resources for AI processing

## Monitoring Services

### Prometheus
**Purpose**: Metrics collection and monitoring system.

**Key Features**:
- Metrics collection from various sources
- Time-series data storage
- Query language (PromQL)
- Alerting rules
- Service discovery
- Data retention policies

**Configuration**:
- **Port**: 9090
- **Data Directory**: `/opt/monitoring/prometheus`
- **Config File**: `/opt/monitoring/prometheus/prometheus.yml`
- **Retention**: 15 days (configurable)

**Access**:
- Web Interface: `http://<host>:9090`
- Query Interface: `http://<host>:9090/graph`
- Targets: `http://<host>:9090/targets`

**Metrics Sources**:
- Node Exporter (system metrics)
- Docker Exporter (container metrics)
- Application metrics (if configured)

### Alertmanager
**Purpose**: Alert management and notification system.

**Key Features**:
- Alert routing and grouping
- Notification channels (email, Slack, etc.)
- Alert silencing
- Alert history
- Integration with Prometheus

**Configuration**:
- **Port**: 9093
- **Data Directory**: `/opt/monitoring/alertmanager`
- **Config File**: `/opt/monitoring/alertmanager/alertmanager.yml`

**Access**:
- Web Interface: `http://<host>:9093`
- Alerts: `http://<host>:9093/#/alerts`
- Silences: `http://<host>:9093/#/silences`

### Grafana
**Purpose**: Data visualization and dashboard platform.

**Key Features**:
- Interactive dashboards
- Data source integration
- Alerting and notifications
- User management
- Plugin ecosystem
- Dashboard sharing

**Configuration**:
- **Port**: 3000
- **Data Directory**: `/opt/monitoring/grafana`
- **Config File**: `/opt/monitoring/grafana/grafana.ini`

**Access**:
- Web Interface: `http://<host>:3000`
- Default Login: `admin` / `admin`

**Data Sources**:
- Prometheus (metrics)
- Loki (logs)
- Additional sources as needed

### Loki
**Purpose**: Log aggregation system for centralized logging.

**Key Features**:
- Log collection and storage
- Log querying and filtering
- Integration with Grafana
- Log retention policies
- Multi-tenant support

**Configuration**:
- **Port**: 3100
- **Data Directory**: `/opt/monitoring/loki`
- **Config File**: `/opt/monitoring/loki/loki.yml`

**Access**:
- API: `http://<host>:3100`
- Query Interface: Via Grafana

## Infrastructure Services

### Docker
**Purpose**: Containerization platform for service deployment.

**Key Features**:
- Container runtime
- Image management
- Network management
- Volume management
- Service orchestration

**Configuration**:
- **Socket**: `/var/run/docker.sock`
- **Data Directory**: `/var/lib/docker`
- **Log Driver**: json-file

**Management**:
- Docker Compose for service orchestration
- Docker networks for service isolation
- Docker volumes for data persistence

### Rclone
**Purpose**: Cloud storage synchronization and backup tool.

**Key Features**:
- Multi-cloud support
- Encryption support
- Sync and backup operations
- Bandwidth limiting
- Retry mechanisms

**Configuration**:
- **Config File**: `~/.config/rclone/rclone.conf`
- **Log File**: `/var/log/rclone.log`

**Supported Providers**:
- Google Drive
- Dropbox
- OneDrive
- Amazon S3
- And many more

## Database Services

### PostgreSQL
**Purpose**: Primary database for Paperless-ngx.

**Key Features**:
- ACID compliance
- Full-text search
- JSON support
- Extensions support
- Backup and recovery

**Configuration**:
- **Port**: 5432 (internal)
- **Database**: `paperless`
- **User**: `paperless`
- **Password**: Configured in environment

**Access**:
- Internal only (Docker network)
- Connection string: `postgresql://paperless:password@db:5432/paperless`

### Redis
**Purpose**: Caching and session storage for Paperless-ngx.

**Key Features**:
- In-memory data store
- Caching
- Session storage
- Pub/Sub messaging
- Persistence options

**Configuration**:
- **Port**: 6379 (internal)
- **Data Directory**: `/data`
- **Memory Limit**: Configurable

**Access**:
- Internal only (Docker network)
- Connection string: `redis://redis:6379/0`

## Web Services

### Nginx
**Purpose**: Reverse proxy and web server for Paperless-ngx.

**Key Features**:
- Reverse proxy
- Load balancing
- SSL termination
- Static file serving
- Gzip compression

**Configuration**:
- **Port**: 8000 (external)
- **Config**: Auto-generated by Docker Compose
- **SSL**: Optional (not configured by default)

**Access**:
- Web Interface: `http://<host>:8000`
- Static Files: Served directly by Nginx

## Service Dependencies

### Paperless Stack
```
Nginx → Paperless Web → PostgreSQL
  ↓         ↓
Redis ← Paperless-GPT
```

### Monitoring Stack
```
Prometheus → Grafana
    ↓          ↓
Alertmanager  Loki
```

### Infrastructure
```
Docker → All Services
Rclone → Backup Operations
```

## Service Health Checks

### Health Check Endpoints

| Service | Health Check URL | Expected Response |
|---------|------------------|-------------------|
| Paperless-ngx | `http://<host>:8000/api/` | 200 OK |
| Paperless-GPT | `http://<host>:8001/health` | 200 OK |
| Prometheus | `http://<host>:9090/-/healthy` | 200 OK |
| Alertmanager | `http://<host>:9093/-/healthy` | 200 OK |
| Grafana | `http://<host>:3000/api/health` | 200 OK |
| Loki | `http://<host>:3100/ready` | 200 OK |

### Health Check Commands

```bash
# Check all services
curl -f http://localhost:8000/api/ && echo "Paperless OK"
curl -f http://localhost:8001/health && echo "Paperless-GPT OK"
curl -f http://localhost:9090/-/healthy && echo "Prometheus OK"
curl -f http://localhost:9093/-/healthy && echo "Alertmanager OK"
curl -f http://localhost:3000/api/health && echo "Grafana OK"
curl -f http://localhost:3100/ready && echo "Loki OK"
```

## Service Logs

### Log Locations

| Service | Log Location | Log Format |
|---------|--------------|------------|
| Paperless-ngx | Docker logs | JSON |
| Paperless-GPT | Docker logs | JSON |
| Prometheus | Docker logs | JSON |
| Alertmanager | Docker logs | JSON |
| Grafana | Docker logs | JSON |
| Loki | Docker logs | JSON |
| System | `/var/log/syslog` | Syslog |

### Log Access Commands

```bash
# Docker service logs
docker-compose logs paperless
docker-compose logs paperless-gpt
docker-compose logs prometheus
docker-compose logs alertmanager
docker-compose logs grafana
docker-compose logs loki

# Follow logs in real-time
docker-compose logs -f paperless
docker-compose logs -f paperless-gpt
```

## Service Configuration

### Environment Variables

#### Paperless-ngx
```bash
PAPERLESS_SECRET_KEY=your_secret_key
PAPERLESS_DB_PASSWORD=your_db_password
PAPERLESS_SUPERUSER_NAME=admin
PAPERLESS_SUPERUSER_EMAIL=admin@example.com
PAPERLESS_SUPERUSER_PASSWORD=your_admin_password
```

#### Paperless-GPT
```bash
OPENAI_API_KEY=your_openai_api_key
PAPERLESS_GPT_LLM_PROVIDER=openai
PAPERLESS_GPT_LLM_MODEL=gpt-4o
PAPERLESS_GPT_OCR_PROVIDER=openai
PAPERLESS_GPT_OCR_MODEL=gpt-4o
```

#### Monitoring
```bash
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=your_grafana_password
PROMETHEUS_RETENTION=15d
LOKI_RETENTION=30d
```

## Service Maintenance

### Regular Maintenance Tasks

1. **Database Maintenance**:
   ```bash
   # PostgreSQL vacuum and analyze
   docker-compose exec db psql -U paperless -d paperless -c "VACUUM ANALYZE;"
   ```

2. **Log Rotation**:
   ```bash
   # Rotate Docker logs
   docker system prune -f
   ```

3. **Backup Verification**:
   ```bash
   # Verify backups
   ansible-playbook ansible/playbooks/verify_backup.yml
   ```

4. **Security Updates**:
   ```bash
   # Update system packages
   ansible-playbook ansible/playbooks/update-system.yml
   ```

### Service Restart Procedures

```bash
# Restart individual services
docker-compose restart paperless
docker-compose restart paperless-gpt
docker-compose restart prometheus
docker-compose restart alertmanager
docker-compose restart grafana
docker-compose restart loki

# Restart all services
docker-compose restart
```

## Troubleshooting

### Common Issues

1. **Service Won't Start**:
   - Check Docker daemon status
   - Verify port availability
   - Check resource availability
   - Review service logs

2. **Database Connection Issues**:
   - Verify PostgreSQL is running
   - Check connection credentials
   - Verify network connectivity

3. **API Key Issues**:
   - Verify OpenAI API key is valid
   - Check API key permissions
   - Verify internet connectivity

4. **Performance Issues**:
   - Monitor resource usage
   - Check database performance
   - Review log files for errors
   - Consider scaling resources

### Debug Commands

```bash
# Check service status
docker-compose ps

# Check resource usage
docker stats

# Check network connectivity
docker network ls
docker network inspect <network_name>

# Check volume usage
docker volume ls
docker volume inspect <volume_name>
```

This comprehensive service documentation provides all the information needed to understand, manage, and troubleshoot the homelab infrastructure services.
