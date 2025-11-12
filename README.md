# Homelab Infrastructure

This repository contains the Ansible playbooks and configuration for managing my homelab infrastructure, including Raspberry Pis and other computers. The project includes automated deployment of Paperless-ngx for document management with encrypted cloud backups.

## Project Structure

```
.
├── ansible/                  # Ansible configuration and playbooks
│   ├── group_vars/          # Group variables
│   ├── host_vars/           # Host-specific variables
│   ├── inventory/           # Inventory files
│   ├── roles/              # Ansible roles
│   └── playbooks/          # Ansible playbooks
├── docs/                    # Additional documentation
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## Network Layout

```mermaid
graph TD
    subgraph "Internet"
        A[Comcast ISP<br/>Internet Provider]
    end
    
    subgraph "Edge"
        B[Nighthawk CM300<br/>DOCSIS 3.1<br/>2.5 Gbps Modem]
    end
    
    subgraph "Core Network"
        C[OPNSense Firewall<br/>i7-7700 • 16GB RAM<br/>192.168.0.1]
        D[Unifi US-48-500W<br/>48-Port Managed Switch<br/>PoE+ Capable]
    end
    
    subgraph "Wireless Infrastructure"
        E[NetGear WAX610<br/>WiFi 6 AX1800<br/>Access Point #1]
        F[NetGear WAX610<br/>WiFi 6 AX1800<br/>Access Point #2]
        G[NetGear WAX610<br/>WiFi 6 AX1800<br/>Access Point #3]
    end
    
    subgraph "Mini Rack"
        I[TP-Link TL-SG105<br/>5-Port Gigabit Switch<br/>Unmanaged]
        H[Raspberry Pi 4B<br/>rpi4b-01<br/>192.168.0.45<br/>Paperless-ngx]
        HL[Raspberry Pi 3B<br/>houselights<br/>192.168.1.121<br/>Holiday Lights Controller]
        J[Raspberry Pi 4B<br/>homeassistant<br/>192.168.0.43<br/>Home Assistant OS]
    end
    
    subgraph "Storage"
        K[NAS Server<br/>i7-9900 • 16GB RAM<br/>10x 3TB HDD<br/>FreeNAS/OpenNAS<br/>Under Construction]
    end
    
    subgraph "Gaming Infrastructure"
        L[3 Desktop Gaming Computers<br/>Wired Connection]
    end
    
    A -.->|Internet| B
    B -->|WAN Port| C
    C -->|LAN Port| D
    D -->|PoE+ Port| E
    D -->|PoE+ Port| F
    D -->|PoE+ Port| G
    D -->|Ethernet Port| I
    D -->|Ethernet Port| K
    D -->|Ethernet Port| L
    I -->|Ethernet Port| H
    I -->|Ethernet Port| HL
    I -->|Ethernet Port| J
    
    style A fill:#1565c0,color:#ffffff,stroke:#0d47a1,stroke-width:2px
    style B fill:#7b1fa2,color:#ffffff,stroke:#4a148c,stroke-width:2px
    style C fill:#388e3c,color:#ffffff,stroke:#1b5e20,stroke-width:2px
    style D fill:#f57c00,color:#ffffff,stroke:#e65100,stroke-width:2px
    style E fill:#c2185b,color:#ffffff,stroke:#880e4f,stroke-width:2px
    style F fill:#c2185b,color:#ffffff,stroke:#880e4f,stroke-width:2px
    style G fill:#c2185b,color:#ffffff,stroke:#880e4f,stroke-width:2px
    style I fill:#795548,color:#ffffff,stroke:#3e2723,stroke-width:2px
    style H fill:#00695c,color:#ffffff,stroke:#004d40,stroke-width:2px
    style HL fill:#ff6f00,color:#ffffff,stroke:#e65100,stroke-width:2px
    style J fill:#4caf50,color:#ffffff,stroke:#2e7d32,stroke-width:2px
    style K fill:#ff9800,color:#ffffff,stroke:#e65100,stroke-width:2px
    style L fill:#673ab7,color:#ffffff,stroke:#4527a0,stroke-width:2px
```

### WiFi/IoT Devices

```mermaid
graph TD
    subgraph "WiFi Infrastructure"
        WIFI[WiFi Access Points<br/>3x NetGear WAX610]
    end
    
    subgraph "Mobile Devices"
        M1[4 Cell Phones • 2 Tablets]
    end
    
    subgraph "Entertainment"
        GC[Gaming Consoles<br/>PS3 • PS4 • PS5<br/>XBox 360 • XBox One<br/>4 Nintendo Switches]
        TV[6 Smart TVs]
        GP[2 WiFi Gaming Desktops]
    end
    
    subgraph "Smart Home"
        S1[Smart Door Nob • Smart Microwave<br/>Smart Dishwasher • WiFi Power Monitor]
        S2[8 Temperature Sensors • 3 Motion Sensors]
        S3[~30 Smart Bulbs]
    end
    
    WIFI -.->|WiFi| M1
    WIFI -.->|WiFi| GC
    WIFI -.->|WiFi| TV
    WIFI -.->|WiFi| GP
    WIFI -.->|WiFi| S1
    WIFI -.->|WiFi| S2
    WIFI -.->|WiFi| S3
    
    style WIFI fill:#c2185b,color:#ffffff,stroke:#880e4f,stroke-width:2px
    style M1 fill:#3f51b5,color:#ffffff,stroke:#283593,stroke-width:2px
    style GC fill:#e91e63,color:#ffffff,stroke:#ad1457,stroke-width:2px
    style TV fill:#ff5722,color:#ffffff,stroke:#d84315,stroke-width:2px
    style GP fill:#795548,color:#ffffff,stroke:#3e2723,stroke-width:2px
    style S1 fill:#9c27b0,color:#ffffff,stroke:#6a1b9a,stroke-width:2px
    style S2 fill:#9c27b0,color:#ffffff,stroke:#6a1b9a,stroke-width:2px
    style S3 fill:#9c27b0,color:#ffffff,stroke:#6a1b9a,stroke-width:2px
```

### Network Components

- **Internet Provider**: Comcast
- **Modem**: Nighthawk CM300 DOCSIS 3.1 (2.5 Gbps)
- **Firewall**: OPNSense running on i7-7700 with 16GB RAM
- **Core Switch**: Unifi US-48-500W (48-port managed switch)
- **WiFi Access Points**: 3x NetGear WAX610 WiFi 6 AX1800
- **Mini Rack Switch**: TP-Link TL-SG105 (5-port gigabit unmanaged switch)
- **Services**: 
  - Raspberry Pi 4B running Paperless-ngx (192.168.0.45)
  - Raspberry Pi 3B running Houselights controller (192.168.1.121)
  - Raspberry Pi 4B running Home Assistant OS (192.168.0.43)
  - NAS Server (i7-9900, 16GB RAM, 10x 3TB HDD, FreeNAS/OpenNAS) - Under Construction
  - 3 Desktop Gaming Computers (Wired)
- **WiFi/IoT Devices**:
  - **Mobile**: 4 Cell Phones, 2 Tablets
  - **Gaming Consoles**: PS3, PS4, PS5, XBox 360, XBox One, 4 Nintendo Switches
  - **Gaming PCs**: 2 WiFi Gaming Desktops
  - **Smart Home**: Smart Door Nob, Smart Microwave, Smart Dishwasher, WiFi Power Monitor
  - **Sensors**: 8 Temperature Sensors, 3 Motion Sensors
  - **Lighting**: ~30 Smart Bulbs
  - **Entertainment**: 6 Smart TVs

### Custom Services
- `rpi4b-01`: Paperless-ngx document management stack
- `houselights`: Holiday lighting controller from [`deathbreakfast/house-lights`](https://github.com/deathbreakfast/house-lights)

## Documentation

For detailed setup and usage instructions, please refer to the [documentation](docs/README.md). The documentation includes:

- Step-by-step setup guides
- Device configuration instructions
- Security best practices
- Troubleshooting guides

## Security

- **Never commit sensitive data** to this repository
- Use Ansible Vault for encrypting sensitive information
- Store secrets in a separate secure location
- Use environment variables for sensitive data when possible

## Requirements

- Ansible 2.9 or later
- Python 3.6 or later
- SSH access to managed nodes

## Getting Started

1. Clone this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create your inventory file in `ansible/inventory/`
4. Set up your SSH keys and access
5. Run your playbooks:
   ```bash
   ansible-playbook -i ansible/inventory/hosts ansible/playbooks/site.yml
   ```

## Inventory

The inventory is organized by device type and location. See `ansible/inventory/` for details.

### Current Devices
- **rpi4b-01** (192.168.0.45) - Raspberry Pi 4B running Paperless-ngx
- **houselights** (192.168.1.121) - Raspberry Pi 3B planned for holiday RGB lighting control

### Houselights Controller
The controller pulls code from [`deathbreakfast/house-lights`](https://github.com/deathbreakfast/house-lights) and runs it as a managed Flask service on the `houselights` Pi.

- Deploy / ensure service is running:
  ```bash
  ansible-playbook -i ansible/inventory/hosts ansible/playbooks/houselights.yml
  ```
- Pull latest code and restart gracefully:
  ```bash
  ansible-playbook -i ansible/inventory/hosts ansible/playbooks/houselights-update.yml
  ```

## Paperless-ngx

This project includes automated deployment of Paperless-ngx, a document management system that helps you go paperless. The deployment includes:

- Docker-based installation with PostgreSQL database
- Redis for task queue management
- OCR capabilities for document text extraction
- Web interface accessible at `http://192.168.0.45:8000`

### Deploying Paperless-ngx

To deploy Paperless-ngx on your Raspberry Pi:

```bash
ansible-playbook -i ansible/inventory/hosts ansible/playbooks/paperless.yml
```

Or include it in the main deployment:

```bash
ansible-playbook -i ansible/inventory/hosts ansible/playbooks/site.yml
```

## Backup System

The project includes an automated backup system for Paperless-ngx with:

- **Encrypted cloud storage** using rclone crypt
- **Automated daily backups** with cron scheduling
- **Automatic retention management** - keeps only 3 most recent backups
- **Backup verification** and integrity checks
- **Restore functionality** with safety measures
- **Multiple cloud providers** supported

### Deploying Backup System

```bash
ansible-playbook -i ansible/inventory/hosts ansible/playbooks/backup.yml
```

**Important**: Configure your cloud storage credentials and encryption passwords in `ansible/group_vars/raspberry_pis.yml` before deployment.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - See LICENSE file for details 