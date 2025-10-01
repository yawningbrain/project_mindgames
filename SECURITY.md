# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Please report (suspected) security vulnerabilities through **GitHub Security Advisories**. You will receive a response within 48 hours. If the issue is confirmed, we will release a patch as soon as possible.

## Security Best Practices

### 1. Credential Management

**Never commit sensitive credentials to the repository!**

- Use `.env` files for local development (already in `.gitignore`)
- Never use example passwords in production
- On macOS, prefer passwordless sudo with proper user restrictions

### 2. macOS Sudo Access

Limit passwordless sudo to only the specific command needed:
```bash
sudo visudo
# Add: USERNAME ALL=(ALL) NOPASSWD: /path/to/venv/bin/python /path/to/main.py
```

### 3. Data Privacy

- EEG data contains sensitive biometric information
- Ensure proper encryption if required by regulations
- Be aware of GDPR/HIPAA compliance

## Contact

For security concerns: Use GitHub Security Advisories

For general issues: GitHub Issues

Last Updated: October 1, 2025
