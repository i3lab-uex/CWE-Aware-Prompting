import re

# Pre‑compiled regex to validate a simple http or https URL.
# It checks for the scheme, '://', and then any non‑whitespace characters
# (which covers most typical URLs).  The pattern is intentionally simple to
# avoid excessive backtracking and potential denial‑of‑service attacks.
_URL_RE = re.compile(r'^(https?://[^\s]+)$', re.IGNORECASE)


def verify_link(link: str) -> bool:
    """
    Determine whether a given string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    link : str
        The string to evaluate as a potential valid URL.

    Returns
    -------
    bool
        True if the string matches the expected URL pattern, False otherwise.

    Notes
    -----
    The function is intentionally conservative: it only checks the presence of a
    scheme and non‑whitespace characters after it.  It does not attempt to resolve
    DNS or verify the host.  This keeps the function lightweight and avoids
    external side‑effects, which also mitigates CWE-664 concerns about resource
    management.
    """
    if not isinstance(link, str):
        return False

    # Using the pre‑compiled regex for efficiency.
    return bool(_URL_RE.match(link))