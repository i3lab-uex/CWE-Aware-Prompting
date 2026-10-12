import re
from urllib.parse import urlparse, ParseResult

# --------------------------------------------------------------------------- #
# Trusted image hosting providers.  Only URLs whose netloc ends with one of
# these suffixes will be accepted.
_TRUSTED_DOMAINS = {
    ".imgur.com",
    ".cloudinary.com",
    ".flickr.com",
    ".photobucket.com",
    ".tinypic.com",
}

# Allowed URL schemes.  We explicitly disallow anything other than http/https.
_ALLOWED_SCHEMES = {"http", "https"}


def _is_trusted_domain(netloc: str) -> bool:
    """
    Return True if *netloc* ends with one of the trusted domain suffixes.
    """
    # Normalize to lowercase for case‑insensitive comparison
    netloc = netloc.lower()
    return any(netloc.endswith(suffix) for suffix in _TRUSTED_DOMAINS)


def validate_image_source(img_src: str) -> str:
    """
    Validate that *img_src* points to a trusted image hosting provider.

    Parameters
    ----------
    img_src : str
        The image URL to validate.

    Returns
    -------
    str
        The original, fully‑qualified URL if it is trusted.

    Raises
    ------
    ValueError
        If the URL uses an unsupported scheme or does not belong to a trusted
        domain.
    """
    if not isinstance(img_src, str):
        raise ValueError("img_src must be a string")

    parsed: ParseResult = urlparse(img_src)

    # Scheme check
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(
            f"Unsupported URL scheme: {parsed.scheme!r}. "
            "Only 'http' and 'https' are allowed."
        )

    # Domain check
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(
            f"Untrusted domain: {parsed.netloc!r}. "
            "Only predefined image hosting providers are allowed."
        )

    # Reconstruct the URL to ensure it is in a canonical form.
    canonical_url = parsed.geturl()
    return canonical_url