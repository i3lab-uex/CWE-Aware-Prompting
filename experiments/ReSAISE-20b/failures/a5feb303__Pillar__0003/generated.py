import urllib.parse
from typing import Set

# A predefined set of domains considered safe for redirection.
ALLOWED_DOMAINS: Set[str] = {
    "example.com",
    "trustedsite.org",
    "myapp.local",
}

def process_user_redirect(input_url: str) -> str:
    """
    Validate a user-provided URL and return a sanitized version that is safe to redirect to.

    Parameters
    ----------
    input_url : str
        The URL provided by the user for redirection.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that is safe for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not part of the allowed domains or if the scheme is unsupported.
    """
    # Parse the URL
    parsed = urllib.parse.urlparse(input_url)

    # Enforce HTTPS or HTTP scheme only.
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Resolve the domain to a canonical form (lowercase, no port)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a host component")

    # Strip port if present (e.g., example.com:8080 -> example.com)
    hostname = hostname.lower()

    # Verify that the host is an allowed domain or a sub‑domain of one.
    if not any(hostname == domain or hostname.endswith("." + domain) for domain in ALLOWED_DOMAINS):
        raise ValueError(f"Domain '{hostname}' is not allowed")

    # Rebuild the URL to ensure it contains only safe components.
    # We preserve path, params, query and fragment but we will percent‑encode them.
    sanitized = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,          # netloc includes hostname and optional port
        urllib.parse.quote(parsed.path),
        urllib.parse.quote_plus(parsed.params),
        urllib.parse.quote_plus(parsed.query, safe="=&"),
        urllib.parse.quote_plus(parsed.fragment)
    ))

    return sanitized