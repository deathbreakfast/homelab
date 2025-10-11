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