# Security Policy

## Reporting a Vulnerability

We take the security of uSipipo Support Bot seriously. If you believe you've found a security vulnerability, please report it to us responsibly.

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: **usipipo@gmail.com**

### What to Include

Please include the following information in your report:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if you have one)
- Your contact information for follow-up

### Response Time

We will acknowledge receipt of your report within **48 hours** and will keep you informed of our progress.

### Security Best Practices

When contributing to this project, please follow these security best practices:

1. **Never commit secrets** - API keys, tokens, passwords should never be committed
2. **Validate all inputs** - Always validate and sanitize user inputs
3. **Use prepared statements** - Never concatenate SQL queries
4. **Keep dependencies updated** - Regularly update dependencies for security patches
5. **Follow least privilege** - Only request necessary permissions
6. **Enable authentication** - All API calls must be authenticated
7. **Log security events** - Log authentication failures and suspicious activities

### Security Features

This bot implements the following security features:

- ✅ JWT authentication with auto-refresh
- ✅ Secure token storage in Redis
- ✅ HTTPS-only API communication
- ✅ Input validation and sanitization
- ✅ Rate limiting (via backend)
- ✅ Audit logging for all operations
- ✅ User isolation (users can only see their own tickets)

Thank you for helping keep uSipipo secure! 🔒
