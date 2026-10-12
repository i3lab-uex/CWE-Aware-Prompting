import re
from urllib.parse import urlparse, urlunparse

# List of fully qualified domain names that are considered trusted.
_TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "storage.googleapis.com",
    # Add more trusted domains here as needed.
}

# Regular expression to validate that the scheme is either http or https.
_SCHEME_RE = re.compile(r"^(http|https)$", re.IGNORECASE)


def validate_image_source(img_src: str) -> str:
    """
    Validate that an image URL originates from a trusted provider.

    Parameters
    ----------
    img_src : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The fully resolved, normalized URL if it is trusted.

    Raises
    ------
    ValueError
        If the URL has an unsupported scheme, is malformed,
        or does not point to a trusted domain.
    """
    # Parse the URL into components
    parsed = urlparse(img_src)

    # 1. Validate scheme (http or https)
    if not _SCHEME_RE.match(parsed.scheme):
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP and HTTPS are allowed.")

    # 2. Ensure netloc (host) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname (netloc).")

    # 3. Check the host against the trusted domain list.
    #   We consider subdomains of a trusted domain as trusted only if they
    #   match the exact domain in the set. This prevents unintended delegation.
    host = parsed.hostname.lower()
    if host not in _TRUSTED_DOMAINS:
        raise ValueError(f"Untrusted domain: '{host}'. Only specific image hosts are allowed.")

    # 4. Reconstruct a normalized URL.
    #   We keep the path, params, query, and fragment unchanged,
    #   but ensure that the scheme and netloc are lower‑cased
    normalized = urlunparse((
        parsed.scheme.lower(),
        host,
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return normalized