import re
from urllib.parse import urlparse, urlunparse

# List of trusted image host domains (add or remove as needed)
TRUSTED_DOMAINS = {
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "picsum.photos",
    # Add more trusted domains here
}

# Allowed URL schemes for image URLs
ALLOWED_SCHEMES = {"http", "https"}


def _is_valid_domain(netloc: str) -> bool:
    """
    Validate that the netloc corresponds to a trusted domain.
    Handles optional port numbers and ignores credentials if present.
    """
    # Strip username:password@ prefix if present
    netloc = re.sub(r"^[^@]+@", "", netloc)

    # Remove port if present
    domain = netloc.split(":")[0].lower()

    return domain in TRUSTED_DOMAINS


def check_image_url(img_address: str) -> str:
    """
    Validate an image URL and return the resolved full URL if it belongs to a trusted
    image hosting provider.

    Parameters
    ----------
    img_address : str
        The input image URL to validate.

    Returns
    -------
    str
        The validated and fully resolved URL.

    Raises
    ------
    ValueError
        If the URL scheme is unsupported, or the domain is not in the trusted list,
        or if the URL is malformed.
    """
    # Parse the incoming URL
    try:
        parsed = urlparse(img_address)
    except Exception as exc:
        raise ValueError(f"Malformed URL: {img_address}") from exc

    # Validate scheme
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate domain
    if not _is_valid_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not trusted")

    # Reconstruct the URL to ensure consistent formatting
    cleaned = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )

    return cleaned