import urllib.parse

# List of trusted image hosting domains (add as needed)
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "picsum.photos",
    "cdn.pixabay.com",
    "example.com",  # placeholder
}

def resolve_image_url(image_url: str) -> str:
    """
    Resolve an image URL only if it belongs to a trusted domain.

    Parameters
    ----------
    image_url : str
        The URL of the image to resolve.

    Returns
    -------
    str
        The normalized (canonicalized) URL if the domain is trusted.

    Raises
    ------
    ValueError
        If the URL's host is not in the trusted domain list or if the URL
        is malformed.
    """
    # Parse the URL and ensure it uses HTTP or HTTPS scheme
    parsed = urllib.parse.urlparse(image_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Reject URLs that use IP addresses or localhost to mitigate SSRF
    hostname = parsed.hostname
    if hostname is None:
        raise ValueError("URL must contain a host component")

    # Basic check for IP addresses (IPv4/IPv6)
    if _is_ip_address(hostname):
        raise ValueError("IP addresses are not allowed in image URLs")

    # Ensure the host is in the trusted list
    if hostname.lower() not in TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: {hostname}")

    # Reconstruct the URL to normalize it (e.g., remove default ports)
    normalized = urllib.parse.urlunparse((
        parsed.scheme,
        hostname.lower(),
        _normalize_path(parsed.path),
        "",  # params
        parsed.query,
        ""   # fragment
    ))
    return normalized


def _is_ip_address(hostname: str) -> bool:
    """Return True if hostname is an IPv4 or IPv6 address."""
    import ipaddress
    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False


def _normalize_path(path: str) -> str:
    """Ensure the path is normalized (e.g., remove duplicate slashes)."""
    return urllib.parse.urljoin("/", path)