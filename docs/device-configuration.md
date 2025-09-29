# Device Configuration

This section covers the configuration of different types of devices in your homelab.

## Raspberry Pi Setup

### Initial Raspberry Pi Setup

1. Download Raspberry Pi OS from the [official website](https://www.raspberrypi.org/software/)
2. Flash the image to an SD card using [Raspberry Pi Imager](https://www.raspberrypi.org/software/)
3. Before booting:
   - Create an empty file named `ssh` in the boot partition to enable SSH
   - Create a `wpa_supplicant.conf` file for WiFi setup (if needed)

### Basic Raspberry Pi Configuration

1. Boot the Raspberry Pi and connect via SSH:
   ```bash
   ssh pi@raspberrypi.local
   ```

2. Change the default password:
   ```bash
   passwd
   ```

3. Update the system:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

4. Set a static IP (optional):
   ```bash
   sudo nano /etc/dhcpcd.conf
   ```
   Add:
   ```ini
   interface eth0
   static ip_address=192.168.1.10/24
   static routers=192.168.1.1
   static domain_name_servers=8.8.8.8 8.8.4.4
   ```

### Configure Sudo Without Password for Ansible

Before adding any device to Ansible, configure sudo access without password prompt:

1. Create or edit the sudoers file for your user:
   ```bash
   sudo visudo -f /etc/sudoers.d/ansible-user
   ```

2. Add the following line (replace `username` with your actual username):
   ```
   username ALL=(ALL) NOPASSWD: ALL
   ```
   For example, for the pi user on Raspberry Pi:
   ```
   pi ALL=(ALL) NOPASSWD: ALL
   ```

   > **Important**: The sudoers file format requires a TAB character (not spaces) between the username and `ALL`. If you copy-paste, make sure to replace any spaces with a tab character, or type it directly in the editor.

3. Save and exit. The file permissions should be 0440 by default.

### Adding Raspberry Pi to Ansible

1. Add the Raspberry Pi to your inventory:
   ```bash
   nano ansible/inventory/hosts
   ```
   Add:
   ```ini
   [raspberry_pis]
   rpi1 ansible_host=192.168.1.10 ansible_user=pi
   ```

2. Test the connection:
   ```bash
   ansible raspberry_pis -m ping
   ```

## Desktop Computer Setup

### Initial Desktop Setup

1. Install Ubuntu Server or your preferred Linux distribution
2. During installation:
   - Create a user with sudo privileges
   - Enable SSH server
   - Set up networking

### Basic Desktop Configuration

1. Update the system:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

2. Install basic packages:
   ```bash
   sudo apt install -y build-essential git curl wget
   ```

### Configure Sudo Without Password for Ansible

Before adding the desktop to Ansible, configure sudo access without password prompt:

1. Create or edit the sudoers file for your user:
   ```bash
   sudo visudo -f /etc/sudoers.d/ansible-user
   ```

2. Add the following line (replace `admin` with your actual username):
   ```
   admin ALL=(ALL) NOPASSWD: ALL
   ```

   > **Important**: The sudoers file format requires a TAB character (not spaces) between the username and `ALL`. If you copy-paste, make sure to replace any spaces with a tab character, or type it directly in the editor.

3. Save and exit. The file permissions should be 0440 by default.

### Adding Desktop to Ansible

1. Add the desktop to your inventory:
   ```bash
   nano ansible/inventory/hosts
   ```
   Add:
   ```ini
   [desktop_computers]
   desktop1 ansible_host=192.168.1.20 ansible_user=admin
   ```

2. Test the connection:
   ```bash
   ansible desktop_computers -m ping
   ```

## Server Setup

### Initial Server Setup

1. Install Ubuntu Server
2. During installation:
   - Create a user with sudo privileges
   - Enable SSH server
   - Set up RAID if needed
   - Configure networking

### Basic Server Configuration

1. Update the system:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

2. Install server packages:
   ```bash
   sudo apt install -y build-essential git curl wget nginx
   ```

### Configure Sudo Without Password for Ansible

Before adding the server to Ansible, configure sudo access without password prompt:

1. Create or edit the sudoers file for your user:
   ```bash
   sudo visudo -f /etc/sudoers.d/ansible-user
   ```

2. Add the following line (replace `admin` with your actual username):
   ```
   admin ALL=(ALL) NOPASSWD: ALL
   ```

   > **Important**: The sudoers file format requires a TAB character (not spaces) between the username and `ALL`. If you copy-paste, make sure to replace any spaces with a tab character, or type it directly in the editor.

3. Save and exit. The file permissions should be 0440 by default.

### Adding Server to Ansible

1. Add the server to your inventory:
   ```bash
   nano ansible/inventory/hosts
   ```
   Add:
   ```ini
   [servers]
   server1 ansible_host=192.168.1.30 ansible_user=admin
   ```

2. Test the connection:
   ```bash
   ansible servers -m ping
   ```

## Running Initial Configuration

After adding all your devices to the inventory, you can run the initial configuration:

```bash
ansible-playbook ansible/playbooks/site.yml
```

This will:
1. Apply common configuration to all hosts
2. Configure device-specific settings
3. Set up users and security
4. Install required packages

## Next Steps

Now that your devices are configured, you can proceed to the [Ansible Basics](ansible-basics.md) section to learn more about managing your homelab with Ansible. 