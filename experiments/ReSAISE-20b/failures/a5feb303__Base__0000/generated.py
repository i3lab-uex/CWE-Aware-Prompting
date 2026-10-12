import re
from urllib.parse import urlparse, urlunparse

# Predefined set of safe domains for redirection
ALLOWED_DOMAINS = {
    "example.com",
    "sub.example.org",
}

# Regex to reject IP addresses and localhost
_IP_RE = re.compile(r"""
    ^(
        (?:[0-9]{1,3}\.){3}[0-9]{1,3}          # IPv4
        |
        \[([a-fA-F0-9:]+)\]                    # IPv6
    )$
""", re.VERBOSE)


def _is_allowed_domain(netloc: str) -> bool:
    """
    Check if the given netloc (host[:port]) is within ALLOWED_DOMAINS.
    """
    host = netloc.split(':')[0].lower()  # strip port

    if _IP_RE.match(host) or host in {"localhost", "127.0.0.1"}:
        return False

    # Exact match
    if host in ALLOWED_DOMAINS:
        return True

    # Sub‑domain match: only allow subdomains of the allowed domains
    for domain in ALLOWED_DOMAINS:
        if host.endswith("." + domain):
            return True

    return False


def process_user_redirect(input_url: str) -> str:
    """
    Validate and sanitize a user‑supplied URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized absolute URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL does not use http/https or its domain is not allowed.
    """
    if not input_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(input_url)

    # Ensure the URL is absolute and uses a safe scheme
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must be absolute with a network location")

    if not _is_allowed_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not allowed")

    # Reconstruct the URL to normalise it (e.g., remove default ports)
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc.lower(),
            parsed.path or "",
            "",  # params
            parsed.query,
            ""   # fragment
        )
    )

    return sanitized