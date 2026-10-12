import urllib.parse
from typing import Iterable

# Example list of allowed callback domains.
ALLOWED_CALLBACK_DOMAINS: set[str] = {
    "example.com",
    "auth.example.org",
}

def build_oauth_redirect_url(
    main_url: str,
    redirect_path: str,
    token_state: str
) -> str:
    """
    Construct a safe OAuth redirect URL.

    Parameters
    ----------
    main_url : str
        The application's base URL (e.g., "https://app.example.com").
    redirect_path : str
        The path for the OAuth callback endpoint (e.g., "/oauth/callback").
    token_state : str
        A unique value to include as a query parameter for CSRF protection.

    Returns
    -------
    str
        The fully qualified redirect URL with the state parameter appended.

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Normalise the base URL and join with the redirect path.
    # urljoin handles missing slashes automatically.
    base = main_url.rstrip("/")
    full_path = urllib.parse.urljoin(base + "/", redirect_path.lstrip("/"))

    # Parse the URL to inspect its components.
    parsed = urllib.parse.urlparse(full_path)

    # Verify that the scheme is HTTP or HTTPS.
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Normalize the hostname for comparison.
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a hostname")

    # Check against allowed domains (case‑insensitive).
    if host.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Domain '{host}' is not allowed for OAuth callbacks")

    # Build the query string with the state parameter.
    query = urllib.parse.urlencode({"state": token_state})
    # Reconstruct the URL with the new query.
    safe_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            query,
            parsed.fragment,
        )
    )

    return safe_url