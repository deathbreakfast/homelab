# Paperless-GPT Ansible Role

This role deploys [paperless-gpt](https://github.com/icereed/paperless-gpt) alongside an existing paperless-ngx installation to provide AI-powered document processing capabilities.

## Prerequisites

### 1. OpenAI API Access
Before deploying paperless-gpt, you need:

1. **OpenAI API Account**: Sign up at [OpenAI](https://platform.openai.com/)
2. **API Key**: Generate an API key from your OpenAI dashboard
3. **Billing**: Ensure your account has billing configured for API usage
4. **Vault Configuration**: Add your API key to Ansible vault

```bash
# Add OpenAI API key to vault
ansible-vault edit inventory/group_vars/all/vault.yml
```

Add:
```yaml
vault_openai_api_key: "sk-your-openai-api-key-here"
```

### 2. Existing Paperless-ngx
This role assumes you already have paperless-ngx deployed and running.

## Configuration

### Default Configuration
The role uses the following default settings:

- **LLM Provider**: OpenAI (cloud processing)
- **LLM Model**: gpt-4o
- **OCR Provider**: OpenAI
- **OCR Model**: gpt-4o (with vision capabilities)
- **Port**: 8080
- **Auto Process**: false (manual processing initially)

### Customization
You can override these settings in your playbook or inventory:

```yaml
vars:
  paperless_gpt_llm_provider: "openai"
  paperless_gpt_llm_model: "gpt-4o-mini"  # Use different OpenAI model
  paperless_gpt_auto_process: true         # Enable auto processing
  paperless_gpt_enhanced_pdf: true         # Enable enhanced PDF features
```

### Vault Variables
For production use, set these in your vault:

```bash
ansible-vault edit inventory/group_vars/all/vault.yml
```

Add:
```yaml
vault_openai_api_key: "sk-your-openai-api-key-here"  # Required for OpenAI
vault_paperless_gpt_username: "admin"
vault_paperless_gpt_password: "secure-password"
```

## Deployment

### Option 1: Deploy with existing paperless playbook
```bash
cd /home/seanorourke/homelab/ansible
ansible-playbook -v playbooks/paperless.yml
```

### Option 2: Deploy paperless-gpt separately
```bash
cd /home/seanorourke/homelab/ansible
ansible-playbook -v playbooks/paperless-gpt.yml
```

## Usage

1. **Access the Web UI**: Navigate to `http://your-host:8080`
2. **Tag Documents**: In paperless-ngx, add the `paperless-gpt` tag to documents you want to process
3. **Generate Suggestions**: Use the web UI to generate AI-powered titles, tags, and correspondents
4. **OCR Processing**: Documents tagged with `paperless-gpt-ocr-auto` will be automatically processed

## Troubleshooting

### Common Issues

1. **OpenAI API Issues**
   - Verify API key is correctly set in vault
   - Check OpenAI account billing and usage limits
   - Ensure API key has sufficient permissions
   - Test API access: `curl -H "Authorization: Bearer YOUR_API_KEY" https://api.openai.com/v1/models`

2. **API Rate Limits**
   - OpenAI has rate limits based on your subscription
   - Consider using `gpt-4o-mini` for lower costs and higher rate limits
   - Adjust `paperless_gpt_token_limit` to manage costs

3. **Network Connectivity**
   - Ensure container can reach OpenAI API (api.openai.com)
   - Check firewall rules if using custom network configuration

4. **Paperless API Connection**
   - Verify paperless-ngx is running and accessible
   - Check credentials match your paperless admin account

### Logs
Check container logs:
```bash
docker logs paperless-gpt
```

## Features

- **AI-Powered Document Titles**: Generate meaningful titles based on content
- **Smart Tagging**: Automatically suggest relevant tags
- **Correspondent Detection**: Identify document senders/recipients
- **Enhanced OCR**: Better text extraction using OpenAI's vision capabilities
- **PDF Enhancement**: Create searchable PDFs with proper text layers

## Integration

Paperless-gpt integrates seamlessly with your existing paperless-ngx installation:

- Shares the same data volumes
- Uses the same document storage
- Appears as an additional service in your docker-compose stack
- Maintains all existing paperless-ngx functionality
