import re

# Regular expression for a reasonably strict but not overly complex email address.
# This pattern matches:
#   - local part: alphanumerics, dots, hyphens, underscores (not consecutive dots)
#   - '@' separator
#   - domain: at least two labels separated by dots, each label starts and ends with an alphanumeric
#   - TLD: 2-63 alphabetic characters (typical)
_EMAIL_RE = re.compile(
    r"^(?P<local>[A-Za-z0-9]+[A-Za-z0-9._+-]*[A-Za-z0-9]+)@"
    r"(?P<domain>(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,63})$"
)

def get_email_domain(addr: str) -> str | None:
    """
    Return the domain part of a valid email address, or None if invalid.

    Parameters
    ----------
    addr : str
        Email address to examine.

    Returns
    -------
    str | None
        Domain portion of the email if valid, otherwise None.
    """
    # Guard against non-string input to avoid TypeError
    if not isinstance(addr, str):
        return None

    match = _EMAIL_RE.fullmatch(addr.strip())
    if not match:
        return None
    return match.group('domain')