import re
from typing import Optional

# Compile the regex once to avoid repeated compilation overhead.
# The pattern validates a simple email structure:
# - local part: one or more non-@, non-whitespace characters
# - @ symbol
# - domain part: labels separated by dots, each label containing letters, digits or hyphens
#   with a top‑level domain of at least two alphabetic characters.
_EMAIL_REGEX = re.compile(
    r"^[^@\s]+@([A-Za-z0-9](?:[A-Za-z0-9\-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9\-]*[A-Za-z0-9])?)+\.[A-Za-z]{2,})$",
    re.IGNORECASE
)

def fetch_email_domain(address: str) -> Optional[str]:
    """
    Return the domain part of a valid email address or None if invalid.

    Parameters
    ----------
    address : str
        The email address to validate and extract the domain from.

    Returns
    -------
    Optional[str]
        The domain string if the email is valid; otherwise None.
    """
    if not isinstance(address, str):
        return None

    match = _EMAIL_REGEX.match(address)
    if not match:
        return None
    # The domain is captured in group 1.
    return match.group(1)