import re
from urllib.parse import urlparse

# List of trusted image hosting domains (exact domain or any sub‑domain)
TRUSTED_DOMAINS = [
    r'^imgur\.com$',
    r'^cdn\.example\.com$',
    r'^images\.myshop\.net$',
]

# Compile the domain patterns for fast matching
_TRUSTED_REGEX = [re.compile(pattern, re.IGNORECASE) for pattern in TRUSTED_DOMAINS]


def _is_trusted_domain(domain: str) -> bool:
    """
    Return True if the given domain matches one of the trusted patterns.
    The check allows sub‑domains (e.g., `sub.imgur.com` is accepted if
    the base domain `imgur.com` is trusted).
    """
    # Normalize the domain (remove trailing dot)
    domain = domain.rstrip('.')
    for regex in _TRUSTED_REGEX:
        if regex.search(domain):
            return True
        # Also accept sub‑domains by checking the suffix after a dot
        if domain.endswith('.' + regex.pattern.strip('^$')):
            return True
    return False


def check_image_url(img_address: str) -> str:
    """
    Validate an image URL and return the original string if it is
    considered safe.

    Parameters
    ----------
    img_address : str
        The input image URL to validate.

    Returns
    -------
    str
        The original URL if it is valid and points to a trusted domain.

    Raises
    ------
    ValueError
        If the URL scheme is unsupported or the domain is not trusted.
    """
    if not isinstance(img_address, str):
        raise ValueError("img_address must be a string")

    # Strip surrounding whitespace
    img_address = img_address.strip()
    if not img_address:
        raise ValueError("img_address cannot be empty")

    parsed = urlparse(img_address)

    # Ensure scheme is http or https
    if parsed.scheme.lower() not in ('http', 'https'):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme!r}")

    # Validate domain
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (domain)")

    if not _is_trusted_domain(parsed.netloc):
        raise ValueError(f"Domain {parsed.netloc!r} is not in the trusted list")

    # The URL passes all checks; return it unchanged
    return img_address