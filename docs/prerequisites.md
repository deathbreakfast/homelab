# Prerequisites

This section covers the basic requirements and installation steps needed to set up your workstation for managing your homelab infrastructure. You'll learn how to install and configure Ubuntu Server, Git, and other essential tools on your management machine.

## Ubuntu Setup

### Installing Ubuntu

1. Download Ubuntu Server LTS from the [official website](https://ubuntu.com/download/server)
2. Create a bootable USB drive using [Rufus](https://rufus.ie/) or [Balena Etcher](https://www.balena.io/etcher/)
3. Boot from the USB drive and follow the installation wizard
4. During installation:
   - Set up a user account with sudo privileges
   - Enable SSH server
   - Choose your preferred disk partitioning

### Basic Ubuntu Configuration

After installation, run these commands to update your system:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y build-essential
```

## Git Installation

Git is required for version control and managing your homelab configuration.

### Installing Git

```bash
sudo apt update
sudo apt install -y git
```

### Configuring Git

Set up your Git identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Verifying Git Installation

Check that Git is installed correctly:

```bash
git --version
```

## Ansible Installation

### Installing Required Packages

First, install the required packages:

```bash
sudo apt update
sudo apt install -y python3-pip python3-dev sshpass
```

### Installing Ansible

Install Ansible using pip:

```bash
sudo pip3 install ansible
```

### Verifying Ansible Installation

Check that Ansible is installed correctly:

```bash
ansible --version
```

### Installing Additional Ansible Tools

Install useful Ansible-related tools:

```bash
sudo pip3 install ansible-lint
```

## Network Configuration

### Setting Up Static IP (Optional)

If you want to set a static IP for your management machine:

1. Edit the network configuration:
   ```bash
   sudo nano /etc/netplan/00-installer-config.yaml
   ```

2. Add your network configuration:
   ```yaml
   network:
     ethernets:
       eth0:
         dhcp4: no
         addresses: [192.168.1.100/24]
         gateway4: 192.168.1.1
         nameservers:
           addresses: [8.8.8.8, 8.8.4.4]
     version: 2
   ```

3. Apply the configuration:
   ```bash
   sudo netplan apply
   ```

## Next Steps

Now that you have the basic requirements installed, you can proceed to the [Initial Setup](initial-setup.md) section to begin configuring your homelab. 