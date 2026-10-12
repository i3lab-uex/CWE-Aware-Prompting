import re
from urllib.parse import urlparse, urlunparse

# List of trusted API domains (case‑insensitive). Add more as needed.
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.trusted.org",
    "data.partner.net",
}

# Regular expression to detect private or loopback IP addresses.
PRIVATE_IP_RE = re.compile(
    r"""
    ^(?:
        # 10.0.0.0 – 10.255.255.255
        (?:10(?:\.\d{1,3}){3})|
        # 172.16.0.0 – 172.31.255.255
        (?:172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})|
        # 192.168.0.0 – 192.168.255.255
        (?:192\.168(?:\.\d{1,3}){2})|
        # Loopback
        (?:127(?:\.\d{1,3}){3})
    )$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the supplied IPv4 address is private or loopback."""
    return bool(PRIVATE_IP_RE.match(ip))

def _is_valid_scheme(parsed: "ParseResult") -> bool:
    """Allow only http or https."""
    return parsed.scheme in {"http", "https"}

def _is_trusted_domain(domain: str) -> bool:
    """Check if the domain (or any of its parent domains) is in TRUSTED_DOMAINS."""
    # Normalise domain to lower case.
    domain = domain.lower()
    # Check direct match or any parent domain (e.g., sub.example.com).
    parts = domain.split(".")
    for i in range(len(parts)):
        candidate = ".".join(parts[i:])
        if candidate in TRUSTED_DOMAINS:
            return True
    return False

def validate_api_endpoint(api_url: str) -> str:
    """
    Validate that `api_url` points to a trusted external API endpoint.

    Parameters
    ----------
    api_url : str
        The URL to validate.

    Returns
    -------
    str
        Normalised, validated URL.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsupported scheme,
        points to a private/internal IP address,
        or does not belong to one of the trusted domains.
    """
    if not isinstance(api_url, str):
        raise ValueError("api_url must be a string")

    # Parse the URL and perform basic validation.
    parsed = urlparse(api_url.strip())
    if not _is_valid_scheme(parsed):
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    # Resolve potential IPv4 literal in netloc.
    host = parsed.hostname
    if not host:
        raise ValueError("Unable to determine hostname from URL")

    # Reject private IP addresses.
    if host.replace(".", "").isdigit():  # quick IPv4 literal check
        if _is_private_ip(host):
            raise ValueError("URL points to a private or loopback IP address")

    # Reject non‑trusted domains.
    if not _is_trusted_domain(host):
        raise ValueError(f"Domain '{host}' is not in the list of trusted domains")

    # Re‑assemble the URL to ensure consistent formatting.
    cleaned = urlunparse(parsed._replace(fragment=""))  # strip fragment
    return cleaned