import re
from urllib.parse import urlparse, urlunparse

# List of trusted image hosting domains (add or remove as needed)
_TRUSTED_DOMAINS = {
    "images.example.com",
    "cdn.trustedsite.org",
    "pics.safehost.net",
}

# Allowed URL schemes
_ALLOWED_SCHEMES = {"http", "https"}

# Compile a regex for domain validation (basic TLD check)
_DOMAIN_REGEX = re.compile(r"^(?P<subdomains>(?:[a-z0-9-]+\.)*)(?P<tld>[a-z]{2,})$", re.IGNORECASE)


def _is_valid_domain(domain: str) -> bool:
    """
    Verify that the domain is syntactically valid and in the trusted list.
    """
    if not _DOMAIN_REGEX.match(domain):
        return False
    # Compare domain in a case‑insensitive manner
    return domain.lower() in _TRUSTED_DOMAINS


def validate_picture_url(pic_url: str) -> str:
    """
    Validate that the provided picture URL uses a trusted host and supported scheme.

    Parameters
    ----------
    pic_url : str
        The image URL to validate.

    Returns
    -------
    str
        The normalized, fully‑qualified URL if it is trusted.

    Raises
    ------
    ValueError
        If the scheme is unsupported, the domain is not trusted,
        or the URL is malformed.
    """
    if not isinstance(pic_url, str):
        raise ValueError("pic_url must be a string")

    parsed = urlparse(pic_url)

    # Ensure the URL has a scheme and netloc
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must contain a scheme and host")

    # Scheme validation
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Domain validation
    host = parsed.hostname
    if not host or not _is_valid_domain(host):
        raise ValueError(f"Untrusted domain: {host}")

    # Re‑assemble the URL to ensure consistency
    cleaned = urlunparse((
        parsed.scheme.lower(),
        host.lower(),
        parsed.path or "",
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    return cleaned