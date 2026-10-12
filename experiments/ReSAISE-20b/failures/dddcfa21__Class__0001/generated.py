import urllib.parse

# List of trusted image host domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "imgur.com",
    "cdn.example.com",
    "images.unsplash.com",
    "i.redd.it",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def check_image_url(img_address: str) -> str:
    """
    Validate an image URL against a list of trusted domains.

    Parameters
    ----------
    img_address : str
        The image URL to validate.

    Returns
    -------
    str
        The validated and resolved absolute URL if it is trusted.

    Raises
    ------
    ValueError
        If the scheme is not HTTP/HTTPS or the host domain is not in TRUSTED_DOMAINS.
    """
    if not isinstance(img_address, str):
        raise ValueError("Image address must be a string")

    # Parse the URL
    parsed = urllib.parse.urlparse(img_address)

    # Validate scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Resolve hostname (handle possible IDN / punycode)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Normalise the domain to lower case for comparison
    host = host.lower()

    # Check if host is exactly in the trusted list or a subdomain of one
    def is_trusted(hostname: str) -> bool:
        if hostname in TRUSTED_DOMAINS:
            return True
        for domain in TRUSTED_DOMAINS:
            if hostname.endswith("." + domain):
                return True
        return False

    if not is_trusted(host):
        raise ValueError(f"Untrusted domain: {host!r}")

    # Reconstruct the URL to ensure it is absolute and normalised
    normalized = urllib.parse.urlunparse((
        parsed.scheme.lower(),
        host,
        urllib.parse.quote(parsed.path, safe="/"),
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return normalized