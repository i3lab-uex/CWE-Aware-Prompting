import urllib.parse
import ipaddress

# List of trusted image hosting domains (exact match or subdomain)
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.example.com",
    # add more domains as needed
}

def _is_trusted_domain(hostname: str) -> bool:
    """
    Check whether the hostname belongs to a trusted domain.
    Subdomains of a trusted domain are allowed if they end with the domain.
    """
    # Reject plain IP addresses (both IPv4 and IPv6)
    try:
        ipaddress.ip_address(hostname)
        return False
    except ValueError:
        pass

    hostname = hostname.lower()
    for domain in TRUSTED_DOMAINS:
        if hostname == domain or hostname.endswith("." + domain):
            return True
    return False

def fetch_image_url(img_url: str) -> str:
    """
    Validate an image URL against a list of trusted domains and return the
    normalized absolute URL.

    Parameters
    ----------
    img_url : str
        The URL to validate and resolve.

    Returns
    -------
    str
        The validated, absolute image URL.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme, points to an untrusted domain,
        or contains a bare IP address.
    """
    # Parse the URL
    parsed = urllib.parse.urlparse(img_url)

    # Scheme must be HTTP or HTTPS
    if parsed.scheme.lower() not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Hostname must be present
    if not parsed.hostname:
        raise ValueError("URL does not contain a hostname")

    # Verify the domain is trusted
    if not _is_trusted_domain(parsed.hostname):
        raise ValueError(f"Untrusted domain: {parsed.hostname!r}")

    # Rebuild the URL to ensure it is absolute and normalized
    normalized = urllib.parse.urlunparse(parsed)
    return normalized