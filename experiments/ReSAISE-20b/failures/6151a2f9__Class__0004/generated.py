import re
from urllib.parse import urlparse, urlunparse

# List of fully qualified trusted image hosting domains.
TRUSTED_DOMAINS = {
    "imgur.com",
    "i.imgur.com",
    "cdn.pixabay.com",
    "images.unsplash.com",
    "placekitten.com",
    "picsum.photos",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

# Regular expression to validate the netloc (domain + optional port)
_NETLOC_RE = re.compile(r"^(?P<host>[^:]+)(?::(?P<port>\d+))?$", re.IGNORECASE)


def _is_trusted_domain(host: str) -> bool:
    """
    Check whether the host (case-insensitive) matches one of the trusted domains.
    The match is performed against the exact domain and any subdomains that
    end with a trusted domain (e.g. foo.imgur.com).
    """
    host = host.lower()
    for td in TRUSTED_DOMAINS:
        if host == td or host.endswith("." + td):
            return True
    return False


def validate_picture_url(pic_url: str) -> str:
    """
    Validate an image URL and return the canonical URL if it belongs to a trusted
    domain.

    Parameters
    ----------
    pic_url : str
        The input image URL to validate.

    Returns
    -------
    str
        The resolved, validated URL.

    Raises
    ------
    ValueError
        If the scheme is unsupported or the domain is not in the trusted list.
    """
    if not isinstance(pic_url, str):
        raise ValueError("pic_url must be a string")

    parsed = urlparse(pic_url)

    # Ensure the scheme is http or https
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Validate netloc (domain + optional port)
    match = _NETLOC_RE.match(parsed.netloc)
    if not match:
        raise ValueError(f"Malformed host in URL: {parsed.netloc}")

    host = match.group("host")
    if not _is_trusted_domain(host):
        raise ValueError(f"Domain '{host}' is not trusted")

    # Reconstruct the URL to ensure it has a standard form
    cleaned = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=host,
    )
    return urlunparse(cleaned)