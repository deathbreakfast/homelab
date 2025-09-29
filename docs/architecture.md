# System Architecture

This document provides an overview of the homelab system architecture, including service relationships, data flow, and infrastructure components.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Management Layer                         │
├─────────────────────────────────────────────────────────────────┤
│  Ansible Control Node (Management Computer)                    │
│  ├── Inventory Management                                       │
│  ├── Playbook Execution                                         │
│  ├── Configuration Management                                   │
│  └── Monitoring & Alerting                                     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Infrastructure Layer                       │
├─────────────────────────────────────────────────────────────────┤
│  Raspberry Pi 4B (Primary Services)                            │
│  ├── Paperless-ngx (Document Management)                        │
│  ├── Paperless-GPT (AI Processing)                            │
│  ├── Prometheus (Metrics Collection)                           │
│  ├── Grafana (Visualization)                                   │
│  ├── Loki (Log Aggregation)                                    │
│  └── Rclone (Cloud Storage)                                    │
├─────────────────────────────────────────────────────────────────┤
│  Desktop Computer (Development & Management)                   │
│  ├── Development Environment                                   │
│  ├── Backup Storage                                            │
│  └── Monitoring Dashboard                                      │
├─────────────────────────────────────────────────────────────────┤
│  Server (Additional Services)                                  │
│  ├── Additional Storage                                        │
│  ├── Backup Services                                           │
│  └── Monitoring Targets                                        │
└─────────────────────────────────────────────────────────────────┘
```

## Service Architecture

### Document Management Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    Paperless-ngx Stack                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Nginx     │  │  Paperless  │  │ PostgreSQL  │             │
│  │ (Port 8000) │  │    Web      │  │  Database   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                │                │                    │
│         └────────────────┼────────────────┘                    │
│                          │                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Redis     │  │ Paperless-  │  │   Tesseract │             │
│  │   Cache     │  │    GPT      │  │     OCR     │             │
│  │             │  │ (Port 8001) │  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

### Monitoring Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    Monitoring Stack                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ Prometheus  │  │Alertmanager │  │   Grafana   │             │
│  │ (Port 9090) │  │ (Port 9093) │  │ (Port 3000) │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                │                │                    │
│         └────────────────┼────────────────┘                    │
│                          │                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Loki      │  │ Node        │  │   Docker    │             │
│  │ (Port 3100) │  │ Exporter    │  │  Exporter   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Architecture

### Document Processing Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Document Processing Flow                      │
├─────────────────────────────────────────────────────────────────┤
│  1. Document Upload                                            │
│     │                                                          │
│     ▼                                                          │
│  2. Paperless-ngx Processing                                   │
│     ├── OCR (Tesseract)                                        │
│     ├── Classification                                         │
│     └── Storage                                                │
│     │                                                          │
│     ▼                                                          │
│  3. Paperless-GPT Enhancement                                  │
│     ├── AI-powered OCR (OpenAI Vision)                         │
│     ├── Document Classification (GPT-4)                       │
│     ├── Content Extraction                                     │
│     └── Metadata Enhancement                                   │
│     │                                                          │
│     ▼                                                          │
│  4. Storage & Indexing                                         │
│     ├── PostgreSQL Database                                    │
│     ├── File System Storage                                    │
│     └── Search Index                                           │
└─────────────────────────────────────────────────────────────────┘
```

### Monitoring Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Monitoring Data Flow                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Hosts     │───▶│ Prometheus  │───▶│   Grafana   │         │
│  │ (Metrics)   │    │ (Collector) │    │ (Dashboard) │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│         │                   │                   │              │
│         ▼                   ▼                   ▼              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Logs      │───▶│    Loki     │───▶│   Grafana   │         │
│  │ (Syslog)    │    │ (Aggregator)│    │ (Log View)  │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## Network Architecture

### Internal Network Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    Network Architecture                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                Docker Networks                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │  Paperless  │  │ Monitoring  │  │   Default   │     │   │
│  │  │   Network   │  │   Network    │  │   Network   │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                │                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                Host Network                             │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │ Raspberry Pi│  │   Desktop    │  │   Server    │     │   │
│  │  │   (Primary) │  │ (Management) │  │ (Storage)   │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Port Allocation

| Service | Port | Protocol | Purpose |
|---------|------|----------|---------|
| Paperless-ngx | 8000 | HTTP | Web interface |
| Paperless-GPT | 8001 | HTTP | AI processing interface |
| Prometheus | 9090 | HTTP | Metrics collection |
| Alertmanager | 9093 | HTTP | Alert management |
| Grafana | 3000 | HTTP | Monitoring dashboard |
| Loki | 3100 | HTTP | Log aggregation |
| Node Exporter | 9100 | HTTP | System metrics |
| Docker Exporter | 9323 | HTTP | Container metrics |

## Storage Architecture

### Data Storage Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    Storage Architecture                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Raspberry Pi Storage                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │ Paperless   │  │ Monitoring  │  │   System    │     │   │
│  │  │   Data      │  │    Data     │  │   Logs      │     │   │
│  │  │ /opt/paperless│ │ /opt/monitoring│ │ /var/log   │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                │                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Cloud Storage (Rclone)                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │   Backups   │  │   Archives  │  │   Sync      │     │   │
│  │  │ /backups    │  │ /archives   │  │ /sync       │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Security Architecture

### Security Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                    Security Architecture                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                Network Security                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │   Firewall  │  │   VPN       │  │   SSH       │     │   │
│  │  │  (UFW)      │  │  (Optional) │  │  Keys      │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                │                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Application Security                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │   Docker    │  │   Secrets    │  │   Access    │     │   │
│  │  │  Security   │  │ Management  │  │  Control    │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                │                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                Data Security                            │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │ Encryption  │  │   Backup     │  │   Access    │     │   │
│  │  │ (At Rest)   │  │  Security   │  │  Logging    │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Backup Architecture

### Backup Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    Backup Architecture                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Local Backup Strategy                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │  Database   │  │   Media     │  │   Config    │     │   │
│  │  │  Backups    │  │   Files     │  │   Files     │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                │                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Cloud Backup Strategy                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │   Rclone    │  │   Scheduled  │  │   Retention │     │   │
│  │  │   Sync      │  │   Backups    │  │   Policy    │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Scalability Considerations

### Horizontal Scaling

```
┌─────────────────────────────────────────────────────────────────┐
│                    Scalability Architecture                    │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Current Setup (Single Node)               │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │ Raspberry Pi│  │   Desktop    │  │   Server    │     │   │
│  │  │ (All Services)│ │ (Management) │  │ (Storage)   │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                │                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Future Scaling (Multi-Node)               │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │   Compute   │  │   Storage   │  │ Monitoring  │     │   │
│  │  │   Nodes     │  │   Nodes     │  │   Nodes     │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Performance Characteristics

### Resource Requirements

| Component | CPU | RAM | Storage | Network |
|-----------|-----|-----|---------|---------|
| Paperless-ngx | Low | 2GB | 10GB+ | Low |
| Paperless-GPT | High | 4GB+ | 5GB | Medium |
| Prometheus | Medium | 1GB | 5GB+ | Medium |
| Grafana | Low | 1GB | 1GB | Low |
| Loki | Medium | 2GB | 10GB+ | Medium |

### Performance Bottlenecks

1. **Paperless-GPT**: AI processing is CPU and memory intensive
2. **Database**: PostgreSQL performance with large document collections
3. **Storage I/O**: File system performance for document storage
4. **Network**: Cloud backup and sync operations

## Disaster Recovery

### Recovery Scenarios

1. **Service Failure**: Individual service restart and recovery
2. **Node Failure**: Complete system restoration from backups
3. **Data Corruption**: Database and file system recovery
4. **Network Failure**: Offline operation and sync when restored

### Recovery Procedures

1. **Service Recovery**: Docker service restart
2. **Data Recovery**: Database and file restoration
3. **Configuration Recovery**: Ansible playbook re-execution
4. **Full System Recovery**: Complete infrastructure rebuild

## Monitoring and Alerting

### Key Metrics

1. **System Metrics**: CPU, RAM, disk, network usage
2. **Application Metrics**: Service health, response times
3. **Business Metrics**: Document processing rates, backup success
4. **Security Metrics**: Failed logins, unauthorized access

### Alerting Rules

1. **Critical**: Service down, disk full, backup failure
2. **Warning**: High resource usage, slow response times
3. **Info**: Successful backups, system updates

This architecture provides a robust, scalable, and maintainable homelab infrastructure that can grow with your needs while maintaining security and performance.
