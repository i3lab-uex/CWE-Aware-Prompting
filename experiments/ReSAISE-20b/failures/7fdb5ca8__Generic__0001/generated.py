import re
from urllib.parse import urlparse

# List of trusted domains (add more as needed)
TRUSTED_DOMAINS = {
    "api.example.com",
    "service.trusted.net",
    "gateway.secure.org"
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"""
    ^
    (?:                 # start non-capturing group for whole IP
        10\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|
        192\.168\.\d{1,3}\.\d{1,3}|
        127\.0\.0\.1
    )
    $
    """,
    re.VERBOSE,
)

# Regex to ensure hostname is a valid FQDN
HOSTNAME_REGEX = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(?:\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*\.?$"
)

def _is_private_ip(host: str) -> bool:
    """Return True if host is a private IP address."""
    return PRIVATE_IP_REGEX.match(host) is not None

def _is_trusted_domain(domain: str) -> bool:
    """Check if domain is in the TRUSTED_DOMAINS set."""
    # Normalise to lowercase and strip trailing dot
    domain = domain.lower().rstrip(".")
    return domain in TRUSTED_DOMAINS

def verify_api_address(url_to_check: str) -> str:
    """
    Validate that the supplied URL points to a trusted external API.

    Parameters
    ----------
    url_to_check : str
        The URL to validate.

    Returns
    -------
    str
        The validated URL (same as input if it passes all checks).

    Raises
    ------
    ValueError
        If the URL is malformed, uses an insecure scheme,
        points to a private IP, or does not belong to a trusted domain.
    """
    parsed = urlparse(url_to_check)

    # Scheme must be https
    if parsed.scheme.lower() != "https":
        raise ValueError("URL scheme must be https")

    # Hostname required
    if not parsed.hostname:
        raise ValueError("URL must contain a hostname")

    host = parsed.hostname

    # Reject private IP addresses
    if _is_private_ip(host):
        raise ValueError("URL points to a private IP address")

    # Reject hostnames that are not valid FQDNs
    if not HOSTNAME_REGEX.match(host):
        raise ValueError("Hostname is not a valid FQDN")

    # Reject internal or sensitive domains
    if not _is_trusted_domain(host):
        raise ValueError(f"Domain '{host}' is not in the list of trusted domains")

    # Ensure there is no user info or port that could be misused
    if parsed.username or parsed.password:
        raise ValueError("URL must not contain user info")

    # Normalise the URL to avoid subtle differences
    normalized_url = parsed.geturl()
    return normalized_url

# Example usage (uncomment to test)
# try:
#     valid = verify_api_address("https://api.example.com/v1/resource")
#     print(f"Valid URL: {valid}")
# except ValueError as e:
#     print(f"Invalid URL: {e}")