import smtplib
import dns.resolver

def verify_email(email):
    """
    Verify the validity of an email address.
    """

    # Split the email address into user and domain parts
    user, domain = email.split('@')

    # Get the MX record for the domain
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = records[0].exchange.to_text()
    except Exception as e:
        return f"Failed to get MX record: {e}"

    # Connect to the SMTP server
    try:
        server = smtplib.SMTP(mx_record)
        server.set_debuglevel(0)
    except Exception as e:
        return f"Failed to connect to SMTP server: {e}"

    # Verify the email address
    try:
        server.helo()
        server.mail('test@example.com')
        code, message = server.rcpt(email)
        server.quit()
        if code == 250:
            return f"{email} is valid."
        else:
            return f"{email} is not valid."
    except Exception as e:
        return f"Failed to verify email: {e}"

# Example usage
email = "samueladebayo@ieee.org"
result = verify_email(email)
print(result)