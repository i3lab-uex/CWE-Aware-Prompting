import re
from urllib.parse import urlparse, urlunparse

# List of approved public API domains (example)
ALLOWED_DOMAINS = {
    "api.example.com",
    "service.mycompany.org",
    "external.partner.net",
}

# Regular expression to match private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"^(?:"
    r"(10(?:\.\d{1,3}){3})|"
    r"(172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})|"
    r"(192\.168(?:\.\d{1,3}){2})|"
    r"(169\.254(?:\.\d{1,3}){2})"
    r")$"
)

def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP address."""
    try:
        parts = host.split(":")[0].split(".")
        if len(parts) != 4:
            return False
        octets = [int(p) for p in parts]
        if not all(0 <= o <= 255 for o in octets):
            return False
        ip = ".".join(map(str, octets))
        return bool(PRIVATE_IP_REGEX.match(ip))
    except ValueError:
        return False

def _normalize_and_validate(url: str) -> str:
    """Normalize the URL and validate its domain."""
    parsed = urlparse(url)

    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError("URL points to a private/internal network")

    # Reject disallowed domains
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not in the allowed list")

    # Reconstruct the URL without user info or fragment
    cleaned = parsed._replace(netloc=parsed.hostname + (f":{parsed.port}" if parsed.port else ""), username=None, password=None, fragment="")
    return urlunparse(cleaned)

def handle_webhook_request(external_url: str) -> str:
    """
    Validate a webhook URL and return it for safe internal API usage.

    Parameters
    ----------
    external_url : str
        The URL supplied by an external service.

    Returns
    -------
    str
        A validated and sanitized URL that can be used for internal API requests.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list or if it points to a private network.
    """
    return _normalize_and_validate(external_url)