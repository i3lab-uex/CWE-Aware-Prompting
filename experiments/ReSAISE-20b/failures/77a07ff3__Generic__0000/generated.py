import re
from urllib.parse import urlparse, urlunparse

# List of approved domains (exact matches). Add your safe domains here.
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.example.net",
}

# Regex to detect IP addresses (IPv4 or IPv6) in the host part.
_IP_REGEX = re.compile(
    r"""
    ^
    (?:
        # IPv4
        (?:\d{1,3}\.){3}\d{1,3}
        |
        # IPv6
        \[
            (?:
                [0-9a-fA-F]{1,4}
                (?:\:[0-9a-fA-F]{1,4}){7}
            |
                (?:[0-9a-fA-F]{1,4}\:){0,7}[0-9a-fA-F]{1,4}
            |
                ::(?:(?:[0-9a-fA-F]{1,4}\:){0,6}[0-9a-fA-F]{1,4})?
            |
                (?:[0-9a-fA-F]{1,4}\:){1,7}:
            |
                :: 
            )
        \]
    )
    $
    """,
    re.VERBOSE,
)

def _is_ip_address(host: str) -> bool:
    """Return True if the host is an IP address (IPv4 or IPv6)."""
    return bool(_IP_REGEX.match(host))

def process_url_redirect(input_url: str) -> str:
    """
    Validate and sanitize a user‑supplied URL for safe redirection.

    Parameters
    ----------
    input_url : str
        The raw URL provided by the user.

    Returns
    -------
    str
        A fully qualified, validated URL that can be safely used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, does not use http/https scheme,
        contains an IP address as host, or its domain is not in the
        approved list.
    """
    if not isinstance(input_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(input_url)

    # Ensure scheme is present and secure
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL scheme must be http or https")

    # Ensure a host is present
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject raw IP addresses to mitigate DNS rebinding attacks
    if _is_ip_address(host):
        raise ValueError("URLs containing raw IP addresses are disallowed")

    # Normalize the host to lowercase for comparison
    normalized_host = host.lower()

    # Verify that the domain is in the approved list.
    # We allow subdomains of approved domains (e.g., sub.example.com)
    if not any(
        normalized_host == domain or normalized_host.endswith("." + domain)
        for domain in APPROVED_DOMAINS
    ):
        raise ValueError(f"Domain '{normalized_host}' is not approved for redirection")

    # Reconstruct the URL to ensure it contains only allowed components.
    safe_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        parsed.fragment or "",
    )
    safe_url = urlunparse(safe_parts)

    return safe_url