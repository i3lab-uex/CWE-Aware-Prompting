import re
from urllib.parse import urlparse, urlunparse

# A predefined set of safe domains (lower‑case)
ALLOWED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "secure.example.net",
}

# Regular expression to validate the URL scheme
_SCHEME_RE = re.compile(r"^(https?)://", re.IGNORECASE)


def _is_allowed_domain(host: str) -> bool:
    """
    Return True if the host (including subdomains) ends with one of the
    allowed domains. The comparison is case‑insensitive.
    """
    host = host.lower()
    for domain in ALLOWED_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return True
    return False


def process_user_redirect(input_url: str) -> str:
    """
    Accept a user supplied URL and return a sanitized version that can be
    safely used for redirection.

    Parameters
    ----------
    input_url : str
        The URL provided by the user for redirection.

    Returns
    -------
    str
        A sanitized, absolute URL that is safe to redirect to.

    Raises
    ------
    ValueError
        If the URL does not use a supported scheme, is malformed,
        or its domain is not in ALLOWED_DOMAINS.
    """
    # 1. Basic syntax check
    if not isinstance(input_url, str) or not input_url:
        raise ValueError("URL must be a non-empty string")

    # 2. Ensure absolute URL with http/https scheme
    if not _SCHEME_RE.match(input_url):
        raise ValueError("URL must start with http:// or https://")

    parsed = urlparse(input_url)

    # 3. Validate scheme
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Unsupported URL scheme")

    # 4. Validate host
    if not parsed.netloc:
        raise ValueError("URL must contain a hostname")

    if not _is_allowed_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not allowed")

    # 5. Reconstruct the URL to normalise it
    sanitized = urlunparse(parsed)

    return sanitized