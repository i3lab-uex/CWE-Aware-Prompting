import re

# Regular expression for a basic but reasonably strict email address.
# It captures the domain part (everything after '@') in group 1.
_EMAIL_RE = re.compile(
    r"^[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+"
    r"(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    r"@(?P<domain>[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
)

def extract_email_domain(email: str) -> str | None:
    """
    Extract the domain part from a valid email address.

    Parameters
    ----------
    email : str
        The input email address to be processed.

    Returns
    -------
    str | None
        The domain part of the email if valid; otherwise, None.
    """
    if not isinstance(email, str):
        return None

    match = _EMAIL_RE.fullmatch(email.strip())
    if match:
        return match.group("domain")
    return None