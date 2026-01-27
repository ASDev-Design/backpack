# Security Considerations

## Overview

Backpack is designed with security as a primary concern. This document outlines security considerations, best practices, and known limitations.

## Security Model

### Threat Model

Backpack protects against:

1. **Credential Exposure**: API keys never stored in plain text
2. **State Tampering**: Encrypted agent.lock files prevent unauthorized modification
3. **Keychain Access**: OS-level keychain provides additional protection
4. **Memory Dumps**: Keys only exist in process memory during execution

### Not Protected Against

1. **Root/Admin Access**: Users with root/admin access can access keychain
2. **Memory Inspection**: Debuggers can inspect process memory
3. **Master Key Exposure**: If `AGENT_MASTER_KEY` is compromised, all data is accessible
4. **Physical Access**: Unencrypted disk access (if master key is stored)

## Encryption Security

### Key Derivation (PBKDF2)

- **Algorithm**: PBKDF2-HMAC-SHA256
- **Iterations**: 100,000 (configurable)
- **Salt**: 16 random bytes per encryption operation
- **Strength**: Resistant to brute force attacks with strong passwords

**Recommendation**: Use a strong `AGENT_MASTER_KEY` (minimum 32 characters, mix of alphanumeric and special characters).

### Symmetric Encryption (Fernet)

- **Algorithm**: AES-128 in CBC mode with HMAC-SHA256 authentication
- **Properties**: Authenticated encryption (confidentiality + integrity)
- **Key Management**: Derived from master key via PBKDF2

**Note**: Fernet uses AES-128. For AES-256, consider using `cryptography.hazmat` primitives directly.

## Keychain Security

### Platform-Specific Considerations

#### macOS
- Uses Keychain Services
- Keys protected by user's login keychain
- Can be unlocked by user password or Touch ID/Face ID
- **Best Practice**: Use separate keychain for production vs development

#### Linux
- Uses Secret Service API (GNOME Keyring or KWallet)
- Unlocked on user login
- **Best Practice**: Set keyring to lock after inactivity

#### Windows
- Uses Windows Credential Manager
- Protected by Windows user account
- **Best Practice**: Use Windows Hello for additional protection

### Registry Security

The keychain registry (`_registry` key) is stored in plain text in the keychain. This is acceptable because:

- It only contains key names (not values)
- Keychain access is already protected
- Needed for list functionality

## Master Key Management

### Current Implementation

- Default: `"default-key"` (INSECURE - for development only)
- Production: Set via `AGENT_MASTER_KEY` environment variable

### Best Practices

1. **Never commit master keys** to version control
2. **Use strong passwords**: Minimum 32 characters, high entropy
3. **Rotate regularly**: Change master key periodically
4. **Separate environments**: Different keys for dev/staging/production
5. **Use secrets management**: Consider tools like HashiCorp Vault, AWS Secrets Manager

### Key Rotation

Currently, key rotation requires:
1. Decrypting all agent.lock files with old key
2. Re-encrypting with new key
3. Updating `AGENT_MASTER_KEY` environment variable

**Future Enhancement**: Implement key rotation utility.

## Agent.lock File Security

### File Permissions

**Recommendation**: Set restrictive permissions on `agent.lock` files:
```bash
chmod 600 agent.lock  # Owner read/write only
```

### Version Control

**Safe to Commit**: Yes, `agent.lock` files are encrypted and safe to commit to Git.

**Not Safe to Commit**:
- `.env` files with plain text secrets
- Master keys
- Unencrypted state files

## Runtime Security

### Environment Variable Injection

- Keys injected into `os.environ` during execution
- Keys exist in process memory only
- Not written to disk in plain text
- **Risk**: Environment variables visible to child processes

### Process Memory

- Keys exist in Python process memory
- Can be inspected with debuggers (gdb, lldb)
- Can be dumped with memory analysis tools
- **Mitigation**: Use secure memory clearing (future enhancement)

### User Consent

- JIT injection requires explicit user consent
- Prevents accidental credential exposure
- **Best Practice**: Review prompts carefully before approving

## Known Limitations

### 1. Default Master Key

The default master key (`"default-key"`) is insecure and should never be used in production.

**Mitigation**: Always set `AGENT_MASTER_KEY` in production environments.

### 2. No Key Rotation

Key rotation requires manual decryption/re-encryption.

**Future Enhancement**: Automated key rotation utility.

### 3. Memory Inspection

Process memory can be inspected by privileged users or debuggers.

**Mitigation**: Use secure memory clearing, consider process isolation.

### 4. Registry Plain Text

The keychain registry stores key names in plain text (though in secure keychain).

**Acceptable**: Only names, not values, and keychain is already protected.

### 5. Single Master Key

All layers use the same master key. Compromise of one layer could compromise all.

**Future Enhancement**: Per-layer key derivation.

## Security Best Practices

### For Developers

1. **Never use default master key** in production
2. **Set strong `AGENT_MASTER_KEY`** environment variable
3. **Restrict file permissions** on agent.lock files
4. **Review consent prompts** before approving key access
5. **Rotate keys periodically**
6. **Use separate keychains** for different environments
7. **Audit keychain access** regularly

### For Teams

1. **Establish key management policy**
2. **Use secrets management tools** for master keys
3. **Implement key rotation schedule**
4. **Train team on security practices**
5. **Monitor keychain access logs** (platform-dependent)
6. **Use separate environments** with different keys

### For Production

1. **Use strong, unique master keys**
2. **Store master keys in secrets manager** (not environment variables)
3. **Implement key rotation automation**
4. **Monitor for unauthorized access**
5. **Use process isolation** for agent execution
6. **Implement audit logging**
7. **Regular security audits**

## Reporting Security Issues

If you discover a security vulnerability, please:

1. **Do not** open a public issue
2. Email security details to [security contact]
3. Include steps to reproduce
4. Allow time for fix before disclosure

## Compliance Considerations

### GDPR

- Keys may contain personal data (API tokens, user IDs)
- Encryption provides technical safeguard
- Consider data retention policies for memory layer

### SOC 2

- Encryption at rest (agent.lock files)
- Access controls (OS keychain)
- Audit trail (keychain access logs)

### HIPAA

- Not designed for PHI storage
- If used with PHI, ensure additional safeguards
- Consider encryption key management requirements

## Security Checklist

Before deploying to production:

- [ ] Strong `AGENT_MASTER_KEY` set (not default)
- [ ] Keychain properly configured
- [ ] File permissions set correctly
- [ ] No plain text secrets in repository
- [ ] Key rotation plan established
- [ ] Monitoring and alerting configured
- [ ] Team trained on security practices
- [ ] Security audit completed
