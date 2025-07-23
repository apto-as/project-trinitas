# Security Policy

## Supported Versions

Claude Code is actively maintained. Security updates are provided for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |

## Reporting a Vulnerability

We take the security of Claude Code seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via [GitHub's security advisory feature](https://github.com/anthropics/claude-code/security/advisories) or by emailing security@anthropic.com.

Please include the following information:

- Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit the issue

We prefer all communications to be in English.

## Security Considerations for Extensions

### Trinitas Extension Security

The Trinitas extension system includes the following security measures:

- **Sandboxed Execution**: Extensions run in isolated environments
- **Permission-Based Access**: Extensions require explicit permissions for file system access
- **Code Review Process**: All extension code is subject to security review
- **Input Validation**: All user inputs are validated and sanitized
- **No Network Access**: Extensions operate locally without external network calls

### Best Practices for Users

When using Claude Code and extensions:

1. **Review Permissions**: Understand what permissions you're granting
2. **Keep Updated**: Always use the latest version with security patches
3. **Limit Scope**: Use the minimum necessary permissions for your tasks
4. **Monitor Activity**: Review logs and outputs for unexpected behavior
5. **Report Issues**: Report any suspicious behavior immediately

## Response Timeline

- **Initial Response**: Within 48 hours of receiving your report
- **Investigation**: We will investigate and provide updates within 5 business days
- **Resolution**: Security patches will be released as soon as possible, typically within 30 days

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine the affected versions
2. Audit code to find any potential similar problems
3. Prepare fixes for all releases still under maintenance
4. Release fixes as quickly as possible

We ask that you:

- Give us reasonable time to investigate and mitigate an issue before making any information public
- Make a good faith effort to avoid privacy violations, destruction of data, and interruption or degradation of our service

## Security Updates

Security updates and advisories will be published:

- [GitHub Security Advisories](https://github.com/anthropics/claude-code/security/advisories)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code/security)

## Contact

For security-related questions or concerns, contact: security@anthropic.com