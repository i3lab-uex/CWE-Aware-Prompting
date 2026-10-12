import re
from urllib.parse import urlparse, urlunparse

# Set of approved domains. Add or remove as needed.
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    # Add other domains here
}

# Regular expression to extract the hostname from a netloc (which may contain port).
_NETLOC_HOSTNAME_RE = re.compile(r"^(?P<host>[^:]+)(?::(?P<port>\d+))?$")


def _extract_hostname(netloc: str) -> str:
    """
    Extracts the hostname part from a netloc string.
    The hostname is lower‑cased and any port information is ignored.
    """
    match = _NETLOC_HOSTNAME_RE.match(netloc)
    if not match:
        raise ValueError(f"Malformed netloc: {netloc!r}")
    return match.group("host").lower()


def _is_approved(hostname: str) -> bool:
    """
    Checks whether the hostname or any of its parent domains
    are in the list of approved domains.
    """
    # Exact match first
    if hostname in APPROVED_DOMAINS:
        return True

    # Check parent domains (e.g., sub.example.com -> example.com)
    parts = hostname.split(".")
    for i in range(1, len(parts)):
        parent_domain = ".".join(parts[i:])
        if parent_domain in APPROVED_DOMAINS:
            return True
    return False


def process_url_redirect(input_url: str) -> str:
    """
    Validates a user supplied URL against a whitelist of approved domains
    and returns the same URL if it is safe.

    Parameters
    ----------
    input_url : str
        The user supplied URL to be validated and redirected.

    Returns
    -------
    str
        A safe-to-use URL for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, missing a scheme, or its domain is not approved.
    """
    if not input_url:
        raise ValueError("URL must not be empty")

    parsed = urlparse(input_url)

    # Ensure the URL has a scheme and is http/https
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme!r}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    hostname = _extract_hostname(parsed.netloc)

    if not _is_approved(hostname):
        raise ValueError(f"Domain '{hostname}' is not approved for redirection")

    # Re‑assemble the URL to ensure normalisation (e.g., strip default ports)
    safe_url = urlunparse(parsed._replace(netloc=hostname))
    return safe_url