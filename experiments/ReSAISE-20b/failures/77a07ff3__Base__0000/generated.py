import re
from urllib.parse import urlparse, urlunparse
import idna

# List of approved domains (example). Extend as needed.
APPROVED_DOMAINS = {
    "example.com",
    "api.example.org",
    "cdn.safe-site.net",
}

# Regular expression to reject private IP ranges and localhost
PRIVATE_IP_RE = re.compile(
    r"""
    ^(                               # start of string
        10\.                              # 10.0.0.0 – 10.255.255.255
      | 127\.                              # localhost
      | 169\.254\.                         # link-local
      | 172\.(1[6-9]|2\d|3[0-1])\.          # 172.16.0.0 – 172.31.255.255
      | 192\.168\.                         # private network
      | 0\.0\.0\.0                          # unspecified
    )\d{1,3}\.\d{1,3}$
    """,
    re.VERBOSE,
)

def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private range."""
    return bool(PRIVATE_IP_RE.match(ip))

def _validate_domain(domain: str) -> None:
    """
    Ensure the domain is approved and not a private IP.
    Raises ValueError if validation fails.
    """
    # Resolve IDNA (punycode) to Unicode
    try:
        unicode_domain = idna.decode(domain)
    except idna.IDNAError as exc:
        raise ValueError(f"Invalid internationalized domain name: {domain}") from exc

    # Reject IP addresses
    if re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", domain):
        if _is_private_ip(domain):
            raise ValueError(f"Domain {domain} is a private IP address")
        # Allow public IPs only if they are in the approved list
        if domain not in APPROVED_DOMAINS:
            raise ValueError(f"Domain {domain} is not approved")
        return

    # Normal hostname
    if unicode_domain.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Domain {unicode_domain} is not approved")

def process_url_redirect(input_url: str) -> str:
    """
    Validate a user-provided URL against an approved domain list and return
    a safe-to-use absolute URL. Raises ValueError if validation fails.
    """
    if not input_url:
        raise ValueError("Empty URL provided")

    parsed = urlparse(input_url)

    # Must be absolute and use http/https
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"URL scheme must be http or https, got '{parsed.scheme}'")

    if not parsed.netloc:
        raise ValueError("URL must contain a network location (netloc)")

    # Ensure the domain is approved
    _validate_domain(parsed.hostname)

    # Reconstruct URL to normalise components (e.g., percent-encoding)
    safe_url = urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc,
            re.sub(r"[?#].*$", "", parsed.path),  # strip query & fragment
            "",  # params are deprecated
            "",  # query is removed for safety
            "",  # fragment is removed
        )
    )

    return safe_url