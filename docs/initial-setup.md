# Initial Setup

This section covers the initial setup of your homelab management environment, including repository setup and SSH configuration.

## Repository Setup

### Cloning the Repository

1. Create a directory for your homelab:
   ```bash
   mkdir ~/homelab
   cd ~/homelab
   ```

2. Clone the repository:
   ```bash
   git clone <repository-url> .
   ```

### Repository Structure

The repository contains the following main directories:

- `ansible/`: Contains all Ansible configuration and playbooks
- `docs/`: Contains this documentation
- `.gitignore`: Specifies which files Git should ignore

## SSH Key Setup

### Generating SSH Keys

1. Generate a new SSH key pair:
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```

2. When prompted:
   - Press Enter to accept the default file location
   - Enter a secure passphrase (recommended)

### Copying SSH Keys to Devices

For each device you want to manage:

1. Copy your public key to the device:
   ```bash
   ssh-copy-id username@device-ip
   ```

2. Test the connection:
   ```bash
   ssh username@device-ip
   ```

### Adding Devices to SSH Config

To make connecting to devices easier:

1. Edit your SSH config:
   ```bash
   nano ~/.ssh/config
   ```

2. Add entries for each device:
   ```config
   Host rpi1
       HostName 192.168.1.10
       User pi
       IdentityFile ~/.ssh/id_ed25519

   Host desktop1
       HostName 192.168.1.20
       User admin
       IdentityFile ~/.ssh/id_ed25519
   ```

## Ansible Configuration

### Setting Up the Inventory

1. Edit the inventory file:
   ```bash
   nano ansible/inventory/hosts
   ```

2. Add your devices:
   ```ini
   [raspberry_pis]
   rpi1 ansible_host=192.168.1.10 ansible_user=pi

   [desktop_computers]
   desktop1 ansible_host=192.168.1.20 ansible_user=admin

   [servers]
   server1 ansible_host=192.168.1.30 ansible_user=admin
   ```

### Testing Ansible Connection

1. Test connection to all devices:
   ```bash
   ansible all -m ping
   ```

2. Test connection to specific groups:
   ```bash
   ansible raspberry_pis -m ping
   ```

## Creating a Python Virtual Environment

It's recommended to use a virtual environment for Python packages:

1. Create a virtual environment:
   ```bash
   python3 -m venv ~/homelab/venv
   ```

2. Activate the virtual environment:
   ```bash
   source ~/homelab/venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Next Steps

Now that your environment is set up, you can proceed to the [Device Configuration](device-configuration.md) section to learn how to configure your specific devices. 