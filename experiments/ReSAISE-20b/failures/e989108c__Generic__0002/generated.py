import re
from urllib.parse import urlparse, urlunparse

# A list of trusted image hosting domains.
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "images.unsplash.com",
    "cdn.pixabay.com",
    "flickr.com",
    "githubusercontent.com",
    # Add more trusted domains as needed
}

# Regular expression to validate that the URL uses http or https.
SCHEME_REGEX = re.compile(r"^(https?)://", re.IGNORECASE)


def get_image_link(link_image: str) -> str:
    """
    Validate that the provided image URL comes from a trusted domain
    and has an allowed scheme (http or https).  If the URL is valid,
    return it unchanged.  Otherwise, raise ValueError.

    Parameters
    ----------
    link_image : str
        The image URL to validate and resolve.

    Returns
    -------
    str
        The original URL if it is trusted and has a valid scheme.

    Raises
    ------
    ValueError
        If the URL is not an HTTP(S) URL or its domain is not in the
        TRUSTED_DOMAINS list.
    """
    if not isinstance(link_image, str):
        raise ValueError("link_image must be a string")

    # Quick scheme check
    if not SCHEME_REGEX.match(link_image):
        raise ValueError("URL must use http or https scheme")

    parsed = urlparse(link_image)

    # Normalize netloc (lowercase, strip port)
    host = parsed.hostname or ""
    host = host.lower()

    # Remove trailing dot (common in DNS names)
    if host.endswith("."):
        host = host[:-1]

    # Check for trusted domain
    if not any(host == d or host.endswith("." + d) for d in TRUSTED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not trusted")

    # Reconstruct the URL to ensure canonical form
    safe_url = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path or "",
            parsed.params or "",
            parsed.query or "",
            parsed.fragment or "",
        )
    )

    return safe_url