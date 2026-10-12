import urllib.parse

# List of domains that are considered trusted image hosts.
TRUSTED_DOMAINS = {
    "imgur.com",
    "cdn.example.com",
    "images.unsplash.com",
    # Add more domains as needed
}


def _is_trusted_domain(host: str) -> bool:
    """
    Return True if the host ends with one of the trusted domains.
    The comparison is case‑insensitive and ignores leading 'www.'.
    """
    host = host.lower()
    if host.startswith("www."):
        host = host[4:]

    return any(host == domain or host.endswith("." + domain) for domain in TRUSTED_DOMAINS)


def resolve_image_url(image_url: str) -> str:
    """
    Resolve an image URL after verifying that its domain is trusted.

    Parameters
    ----------
    image_url : str
        The URL to resolve.

    Returns
    -------
    str
        The resolved absolute URL if the domain is trusted.

    Raises
    ------
    ValueError
        If the URL does not belong to a trusted domain or is malformed.
    """
    if not isinstance(image_url, str):
        raise ValueError("image_url must be a string")

    parsed = urllib.parse.urlparse(image_url)

    # Basic sanity checks
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {image_url!r}")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Untrusted domain: {parsed.netloc!r}")

    # Reconstruct the URL to ensure it is absolute and canonical
    resolved = urllib.parse.urlunparse(parsed)
    return resolved