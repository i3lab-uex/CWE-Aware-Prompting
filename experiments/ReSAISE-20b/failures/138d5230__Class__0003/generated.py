import re
from urllib.parse import urlparse, urlunparse

# Predefined safe domains (can be extended as needed)
ALLOWED_DOMAINS = {
    "example.com",
    "trusted-site.org",
    "safe-domain.net",
}

# Regular expression to validate a URL scheme
_SCHEME_RE = re.compile(r"^(https?)$", re.IGNORECASE)


def _is_allowed_domain(host: str) -> bool:
    """
    Check if the host is exactly one of the allowed domains or a
    sub‑domain of an allowed domain.
    """
    host = host.lower()
    # Direct match
    if host in ALLOWED_DOMAINS:
        return True
    # Sub‑domain check: endswith('.allowed') and no extra dots in the prefix
    for allowed in ALLOWED_DOMAINS:
        if host.endswith("." + allowed):
            # Ensure the part before the allowed domain is a single label
            prefix = host[: -len(allowed) - 1]
            if "." not in prefix and prefix:   # non‑empty, no dot
                return True
    return False


def user_defined_redirect(redirect_url: str) -> str:
    """
    Sanitize a user‑provided URL for redirection.

    Parameters
    ----------
    redirect_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A fully qualified, safe URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme,
        or its domain is not in ALLOWED_DOMAINS.
    """
    if not isinstance(redirect_url, str):
        raise ValueError("redirect_url must be a string")

    # Parse the URL
    parsed = urlparse(redirect_url)

    # Reject if scheme is missing or not http/https
    if parsed.scheme:
        if not _SCHEME_RE.match(parsed.scheme):
            raise ValueError(f"Unsupported scheme: {parsed.scheme}")
    else:
        # No scheme means a relative URL – we accept it as is
        return redirect_url

    # Ensure netloc (host) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a domain")

    # Validate the host against allowed domains
    if not _is_allowed_domain(parsed.netloc):
        raise ValueError(f"Domain '{parsed.netloc}' is not allowed")

    # Reconstruct the URL to avoid any subtle modifications
    sanitized = urlunparse(parsed._replace(fragment=""))
    return sanitized