# Git Setup Guide

This guide covers setting up Git for the homelab project with proper security practices.

## Security Considerations

### ✅ **Already Secured**
- **Vault files**: Sensitive data is encrypted in `ansible/inventory/group_vars/*/vault.yml`
- **Placeholder credentials**: Hardcoded values are clearly marked as "changeme" placeholders
- **Comprehensive .gitignore**: Excludes sensitive files and directories

### 🔒 **Vault Variables**
The following sensitive variables should be set in your vault files:

#### **All Hosts Vault** (`ansible/inventory/group_vars/all/vault.yml`)
```yaml
# OpenAI API Key for Paperless-GPT
vault_openai_api_key: "your_openai_api_key_here"

# Rclone Cloud Storage Credentials
vault_gdrive_client_id: "your_google_drive_client_id"
vault_gdrive_client_secret: "your_google_drive_client_secret"
vault_rclone_crypt_password: "your_encryption_password"
vault_rclone_crypt_salt: "your_encryption_salt"

# Grafana Admin Credentials
vault_grafana_admin_user: "admin"
vault_grafana_admin_password: "your_grafana_password"
```

#### **Raspberry Pi Vault** (`ansible/inventory/group_vars/raspberry_pis/vault.yml`)
```yaml
# Paperless-ngx Credentials
vault_paperless_secret_key: "your_django_secret_key"
vault_paperless_db_password: "your_database_password"
vault_paperless_superuser_password: "your_admin_password"

# Paperless-GPT API Token
vault_paperless_gpt_api_token: "your_paperless_api_token"
```

## Git Repository Setup

### 1. Initialize Git Repository
```bash
cd /home/seanorourke/homelab
git init
```

### 2. Configure Git User (if not already set)
```bash
git config user.name "Sean O'Rourke"
git config user.email "your-email@example.com"
```

### 3. Add Remote Repository (Optional)
```bash
# Add your remote repository
git remote add origin https://github.com/yourusername/homelab.git

# Or if using SSH
git remote add origin git@github.com:yourusername/homelab.git
```

### 4. Initial Commit
```bash
# Add all files (respecting .gitignore)
git add .

# Create initial commit
git commit -m "Initial homelab infrastructure setup

- Complete Ansible roles and playbooks
- Document management with Paperless-ngx and GPT
- Monitoring stack with Prometheus, Grafana, and Loki
- Comprehensive backup and restore system
- Multi-device support (Raspberry Pi, desktop, server)
- Security with Ansible Vault for sensitive data
- Full documentation and architecture guides"
```

### 5. Push to Remote (if configured)
```bash
git branch -M main
git push -u origin main
```

## File Structure in Git

### ✅ **Included in Git**
```
homelab/
├── ansible/                    # Ansible configuration
│   ├── roles/                  # Custom roles
│   ├── playbooks/             # Playbooks
│   ├── inventory/              # Host inventory
│   │   ├── hosts              # Host definitions
│   │   └── group_vars/        # Group variables
│   │       ├── all/           # All hosts variables
│   │       │   └── vars.yml   # Public variables
│   │       └── raspberry_pis/ # Raspberry Pi variables
│   │           └── vars.yml   # Public variables
│   └── requirements.yml       # Ansible dependencies
├── docs/                      # Documentation
├── README.md                  # Project overview
├── requirements.txt           # Python dependencies
└── .gitignore                # Git ignore patterns
```

### ❌ **Excluded from Git**
```
# Vault files (encrypted sensitive data)
ansible/inventory/group_vars/*/vault.yml

# Python virtual environment
ansible_env/

# Local data directories
/opt/paperless/
/opt/monitoring/
/opt/backups/

# Temporary files
*.backup
*.bak
*.tmp
*.temp

# SSH keys and certificates
*.pem
*.key
*.crt
*.p12
id_rsa*
id_ed25519*

# Cloud provider credentials
.aws/
.gcp/
.azure/

# Database dumps
*.sql
*.dump
```

## Security Best Practices

### 1. **Never Commit Sensitive Data**
- All passwords, API keys, and secrets are in vault files
- Vault files are encrypted and excluded from git
- Placeholder values are clearly marked as "changeme"

### 2. **Vault File Management**
```bash
# Edit vault files
ansible-vault edit ansible/inventory/group_vars/all/vault.yml
ansible-vault edit ansible/inventory/group_vars/raspberry_pis/vault.yml

# View vault files
ansible-vault view ansible/inventory/group_vars/all/vault.yml

# Create new vault file
ansible-vault create ansible/inventory/group_vars/new_group/vault.yml
```

### 3. **Vault Password Management**
```bash
# Set vault password file (recommended)
echo "your_vault_password" > ansible/.vault_pass
chmod 600 ansible/.vault_pass

# Use with playbooks
ansible-playbook playbook.yml --vault-password-file ansible/.vault_pass
```

### 4. **Environment-Specific Configuration**
- **Development**: Use placeholder values for testing
- **Production**: Use vault variables with real credentials
- **CI/CD**: Use environment variables or secure vault storage

## Workflow Recommendations

### 1. **Development Workflow**
```bash
# 1. Make changes to roles/playbooks
# 2. Test with placeholder credentials
ansible-playbook playbooks/paperless.yml --check

# 3. Update vault files with real credentials
ansible-vault edit ansible/inventory/group_vars/raspberry_pis/vault.yml

# 4. Test with real credentials
ansible-playbook playbooks/paperless.yml

# 5. Commit changes
git add .
git commit -m "Update paperless configuration"
git push
```

### 2. **Production Deployment**
```bash
# 1. Pull latest changes
git pull

# 2. Update vault files with production credentials
ansible-vault edit ansible/inventory/group_vars/raspberry_pis/vault.yml

# 3. Deploy to production
ansible-playbook playbooks/site.yml --vault-password-file ansible/.vault_pass
```

### 3. **Backup and Recovery**
```bash
# Backup vault files (store securely)
cp ansible/inventory/group_vars/*/vault.yml /secure/backup/location/

# Restore vault files
cp /secure/backup/location/vault.yml ansible/inventory/group_vars/all/
```

## Troubleshooting

### Common Issues

1. **Vault Password Issues**:
   ```bash
   # Reset vault password
   ansible-vault rekey ansible/inventory/group_vars/all/vault.yml
   ```

2. **Git Ignore Not Working**:
   ```bash
   # Check if files are already tracked
   git ls-files | grep vault
   
   # Remove from tracking if needed
   git rm --cached ansible/inventory/group_vars/all/vault.yml
   ```

3. **Sensitive Data in History**:
   ```bash
   # Remove sensitive data from git history
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch ansible/inventory/group_vars/all/vault.yml' \
   --prune-empty --tag-name-filter cat -- --all
   ```

### Security Checklist

- [ ] All vault files are encrypted and excluded from git
- [ ] No hardcoded credentials in plain text files
- [ ] Placeholder values are clearly marked as "changeme"
- [ ] SSH keys and certificates are excluded
- [ ] Cloud provider credentials are excluded
- [ ] Database dumps are excluded
- [ ] Local data directories are excluded
- [ ] Vault password is stored securely
- [ ] Regular backups of vault files
- [ ] Team members have access to vault passwords

## Next Steps

1. **Initialize Git Repository**: Run the git setup commands above
2. **Configure Vault Files**: Add your real credentials to vault files
3. **Test Deployment**: Run playbooks with vault variables
4. **Set Up CI/CD**: Configure automated deployment (optional)
5. **Documentation**: Keep this guide updated with any changes

Your homelab is now ready for secure version control with Git! 🚀
