import re
from urllib.parse import urlparse, urlunparse

# Predefined safe domains.  Add any additional allowed hosts here.
ALLOWED_DOMAINS = {
    "example.com",
    "www.example.com",
    "subdomain.safe.org",
}

# Regular expression to validate URLs minimally (scheme, netloc).
URL_REGEX = re.compile(
    r"^(?P<scheme>https?)://(?P<netloc>[^/]+)(?P<path>/.*)?$",
    re.IGNORECASE,
)

def user_defined_redirect(redirect_url: str) -> str:
    """
    Accept a user‑supplied URL and return a sanitized, safe redirect URL.
    
    Parameters
    ----------
    redirect_url : str
        The user‑supplied URL to validate and potentially return.

    Returns
    -------
    str
        The sanitized absolute URL if it is safe for redirection.

    Raises
    ------
    ValueError
        If the URL does not conform to expectations or its domain is not allowed.
    """
    # Quick sanity check: non‑empty string
    if not redirect_url or not isinstance(redirect_url, str):
        raise ValueError("Redirect URL must be a non‑empty string")

    # Parse the URL
    parsed = urlparse(redirect_url)

    # Ensure scheme is http or https and netloc is present
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        raise ValueError("URL must have http or https scheme and a valid host")

    # Normalize the netloc (lowercase, strip port if default)
    hostname = parsed.hostname.lower() if parsed.hostname else ""
    # Reject URLs with port numbers that are not the default for http/https
    if parsed.port and ((parsed.scheme == "http" and parsed.port != 80) or
                        (parsed.scheme == "https" and parsed.port != 443)):
        raise ValueError("Non‑default port numbers are not allowed")

    # Check that the hostname is in the allowed list
    if hostname not in ALLOWED_DOMAINS:
        raise ValueError(f"Domain '{hostname}' is not allowed for redirection")

    # Reconstruct a clean URL without fragment or query parameters
    safe_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path or "/",
        "",  # params
        "",  # query
        "",  # fragment
    )
    safe_url = urlunparse(safe_parts)

    return safe_url