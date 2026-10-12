import re

# Regular expression pattern for a basic but reasonably strict email address.
# It allows:
#   - local part: letters, digits, underscores, periods and hyphens,
#     but not starting or ending with a period.
#   - domain part: letters, digits, hyphens and periods,
#     with at least one period separating labels.
EMAIL_RE = re.compile(
    r"^(?P<local>[A-Za-z0-9]+[A-Za-z0-9._+-]*[A-Za-z0-9]+)@(?P<domain>[A-Za-z0-9.-]+\.[A-Za-z]{2,})$"
)

def get_email_domain(addr: str):
    """
    Return the domain part of a valid email address or None if invalid.

    Parameters
    ----------
    addr : str
        The email address to examine.

    Returns
    -------
    str | None
        Domain part if the address matches a basic email pattern; otherwise None.
    """
    # Ensure input is a string
    if not isinstance(addr, str):
        return None

    match = EMAIL_RE.fullmatch(addr)
    if not match:
        return None

    # The domain part is captured in the named group 'domain'
    return match.group('domain')