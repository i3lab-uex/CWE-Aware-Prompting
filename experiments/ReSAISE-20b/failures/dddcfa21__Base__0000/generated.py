import re
from urllib.parse import urlparse, urlunparse

# --------------------------------------------------------------------------- #
# Trusted image hosting domains – add or remove as needed.
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "cdn.example.com",
    "images.unsplash.com",
    # add more domains here
}
# --------------------------------------------------------------------------- #

def _is_valid_scheme(scheme: str) -> bool:
    """Return True if the scheme is http or https."""
    return scheme.lower() in {"http", "https"}

def _is_trusted_domain(netloc: str) -> bool:
    """
    Verify that the hostname (netloc) is either exactly a trusted domain
    or ends with one of the trusted domains preceded by a dot.
    """
    # Remove any port
    host = netloc.split(":")[0].lower()
    if host in TRUSTED_DOMAINS:
        return True
    for domain in TRUSTED_DOMAINS:
        if host.endswith("." + domain):
            return True
    return False

def _normalize_url(parsed: "ParseResult") -> str:
    """
    Reconstruct the URL ensuring that we keep only the scheme, netloc,
    path, query and fragment parts – no userinfo or params.
    """
    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path or "",
        "",  # params are deprecated in URLs
        parsed.query,
        parsed.fragment,
    ))

def check_image_url(img_address: str) -> str:
    """
    Validate that the supplied image URL points to a trusted host
    and uses http/https. If valid, return the fully qualified URL.
    
    Parameters
    ----------
    img_address : str
        The image URL to validate.

    Returns
    -------
    str
        The normalized, fully qualified URL.

    Raises
    ------
    ValueError
        If the scheme is unsupported, or the host is not in the trusted list,
        or if the URL is malformed.
    """
    if not isinstance(img_address, str):
        raise ValueError("img_address must be a string")

    # Parse the URL
    parsed = urlparse(img_address)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must be absolute and contain scheme & netloc")

    if not _is_valid_scheme(parsed.scheme):
        raise ValueError(f"Unsupported scheme: {parsed.scheme!r}")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Domain {parsed.netloc!r} is not trusted")

    # Additional security check: disallow URLs that resolve to private IPs
    # (simple regex; for production, consider using socket.gethostbyname)
    if re.match(r"^(127\.|10\.|192\.168\.|172\.(1[6-9]|2\d|3[0-1])\.)", parsed.netloc):
        raise ValueError("Private IP addresses are not allowed")

    # Return the normalized URL
    return _normalize_url(parsed)

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test):
#
# try:
#     print(check_image_url("https://i.imgur.com/example.png"))
# except ValueError as e:
#     print(f"Invalid URL: {e}")