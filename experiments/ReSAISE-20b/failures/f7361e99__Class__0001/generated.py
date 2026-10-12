import re

# Pre‑compiled, non‑backtracking regex for extracting the domain part.
# The pattern matches a single '@' followed by a valid domain:
#   - labels separated by dots, each label starting and ending with an alphanum,
#   - top‑level domain (TLD) at least two letters.
_DOMAIN_RE = re.compile(
    r"^[^@]+@(?P<domain>[A-Za-z0-9](?:[A-Za-z0-9\-]*[A-Za-z0-9])?(?:\.[A-Za-z]{2,})+$"
)

def extract_email_domain(email: str) -> str | None:
    """
    Return the domain part of a valid email address, or None if invalid.

    The function uses a pre‑compiled regular expression that does not
    exhibit catastrophic backtracking. It matches only a single '@'
    and ensures the domain consists of valid labels followed by a TLD.

    Parameters
    ----------
    email : str
        The email address to validate and extract the domain from.

    Returns
    -------
    str | None
        The extracted domain if `email` is a valid address; otherwise, None.
    """
    match = _DOMAIN_RE.match(email)
    return match.group("domain") if match else None