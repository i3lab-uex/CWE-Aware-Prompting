import urllib.parse
from typing import Set

# Allowed domains for OAuth callbacks (example values)
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    "myapp.local"
}

def build_oauth_redirect_url(main_url: str, redirect_path: str, nonce: str) -> str:
    """
    Build a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://app.example.com").
    redirect_path : str
        The path that should be appended to the base URL (e.g., "/auth/callback").
    nonce : str
        A cryptographically random string used as the state parameter.

    Returns
    -------
    str
        The fully qualified OAuth redirect URL including the `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Ensure main_url has a scheme; default to https if missing
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme:
        parsed_main = parsed_main._replace(scheme="https")

    # Resolve the full URL using urljoin to handle relative paths correctly
    joined = urllib.parse.urljoin(urllib.parse.urlunparse(parsed_main), redirect_path)

    # Parse the resulting URL to inspect its domain
    parsed = urllib.parse.urlparse(joined)
    if not parsed.netloc:
        raise ValueError("Constructed URL does not contain a domain")

    # Normalise the hostname (lowercase, remove port)
    host = parsed.hostname.lower() if parsed.hostname else ""

    # Reject URLs that point to disallowed domains
    if host not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(f"Unauthorized callback domain: {host}")

    # Build query parameters, preserving any existing ones
    qs = urllib.parse.parse_qs(parsed.query)
    qs["state"] = [nonce]  # override or add state

    # Reconstruct the URL with updated query string
    new_query = urllib.parse.urlencode(qs, doseq=True)
    final_url_parts = (
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    )
    return urllib.parse.urlunparse(final_url_parts)