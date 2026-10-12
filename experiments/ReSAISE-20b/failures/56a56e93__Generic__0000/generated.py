import re

# Pre‑compiled regex for a simple but reasonable email validation.
# It allows common characters in the local part and ensures
# that a domain is present with at least one dot.
_EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}$"
)

def fetch_email_domain(address: str) -> str | None:
    """
    Return the domain part of a valid e‑mail address.

    Parameters
    ----------
    address : str
        The email address to process.

    Returns
    -------
    str | None
        Domain part if the address is syntactically valid; otherwise None.
    """
    if not isinstance(address, str):
        return None

    match = _EMAIL_REGEX.match(address)
    if not match:
        return None

    # The regex captures the entire domain in group 1
    return match.group(1)