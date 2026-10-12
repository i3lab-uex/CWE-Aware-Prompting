import re
from typing import Optional

# A simple, non‑backtracking regex that captures the domain part of a well‑formed email.
# It matches:
#   * one or more characters that are not '@' (the local part)
#   * a single '@'
#   * the domain: labels separated by dots, ending with a top‑level domain of at least two letters.
# This pattern is deliberately strict to avoid excessive backtracking and keep the
# complexity linear in the length of the input.
_EMAIL_DOMAIN_RE = re.compile(
    r'^[^@]+@(?P<domain>[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+$'
)

def retrieve_email_domain(email_str: str) -> Optional[str]:
    """
    Extract the domain part of a well‑formed email address.

    Parameters
    ----------
    email_str : str
        The email address to parse.

    Returns
    -------
    Optional[str]
        The domain portion of the email if the address is valid, otherwise None.
    """
    try:
        match = _EMAIL_DOMAIN_RE.match(email_str)
        if not match:
            return None
        # The named group 'domain' holds the captured domain.
        return match.group('domain')
    except Exception:
        # Defensive: any unexpected error results in a safe None return.
        return None