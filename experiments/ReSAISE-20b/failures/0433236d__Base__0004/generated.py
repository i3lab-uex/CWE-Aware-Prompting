import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of approved public API domains (case‑insensitive)
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.company.org",
    "public.api.service.net",
}

# Regular expression to quickly reject obvious private IPs or localhost
PRIVATE_IP_PATTERN = re.compile(
    r"^(?:127\.0\.0\.1|"
    r"(?:10(?:\.\d{1,3}){3})|"
    r"(?:172\.1[6-9]|172\.2\d|172\.3[0-1])(?:\.\d{1,3}){2}|"
    r"(?:192\.168)(?:\.\d{1,3}){2}|"
    r"0\.0\.0\.0|"
    r"::1)$",
    re.IGNORECASE,
)

def _is_private_ip(host: str) -> bool:
    """
    Return True if the host resolves to a private IP address.
    The function attempts a quick regex check first, then falls back
    to ipaddress parsing if the host looks like an IP literal.
    """
    # Direct numeric IP check
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not a literal IP, just check for obvious localhost patterns
        return bool(PRIVATE_IP_PATTERN.match(host))

def _is_allowed_domain(domain: str) -> bool:
    """
    Check if the domain (case‑insensitive) is in the allowed list.
    Subdomains are not automatically allowed; only exact matches.
    """
    return domain.lower() in ALLOWED_DOMAINS

def handle_webhook_request(external_url: str) -> str:
    """
    Validate a URL supplied by an external service before using it for
    internal API requests.

    Parameters:
        external_url (str): The URL provided by the external caller.

    Returns:
        str: A validated, normalized URL that can safely be used internally.

    Raises:
        ValueError: If the URL is malformed, uses a disallowed domain,
                    or points to an internal/private network.
    """
    if not isinstance(external_url, str):
        raise ValueError("URL must be a string")

    parsed = urlparse(external_url)

    # Basic scheme check
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http and https schemes are allowed")

    # Ensure netloc (host:port) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Separate host and port
    host, _, port = parsed.netloc.partition(":")
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Reject obvious private IP patterns
    if _is_private_ip(host):
        raise ValueError("URL points to a private or loopback IP address")

    # Reject disallowed domains
    if not _is_allowed_domain(host):
        raise ValueError(f"Domain '{host}' is not in the allowed list")

    # Normalise path, query and fragment to avoid hidden redirects
    cleaned = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=f"{host.lower()}{':' + port if port else ''}",
    )
    validated_url = urlunparse(cleaned)

    return validated_url