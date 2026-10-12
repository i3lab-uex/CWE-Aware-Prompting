import urllib.parse

# List of trusted image hosting domains (add/remove as needed)
_TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.example.com",          # replace with your trusted domains
    "images.unsplash.com",
    "flickr.com",
}

def _is_trusted_domain(domain: str) -> bool:
    """
    Check if the given domain is in the list of trusted domains.
    Supports subdomains by checking suffix match.
    """
    # Normalize to lowercase
    domain = domain.lower()
    for trusted in _TRUSTED_DOMAINS:
        if domain == trusted or domain.endswith("." + trusted):
            return True
    return False

def get_image_link(link_image: str) -> str:
    """
    Validate and resolve an image URL against a list of trusted providers.

    Parameters
    ----------
    link_image : str
        The image URL to validate.

    Returns
    -------
    str
        The original, fully‑qualified URL if it is trusted.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme or points to an untrusted domain.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    parsed = urllib.parse.urlparse(link_image)

    # 1. Ensure scheme is http or https
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # 2. Ensure a network location (host) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host")

    # 3. Validate domain against the trusted list
    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc!r}")

    # 4. Reconstruct the URL to ensure it is absolute and normalized
    resolved_url = urllib.parse.urlunparse(parsed)

    return resolved_url