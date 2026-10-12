#!/usr/bin/env python3
"""
Utility to assemble a secure OAuth callback URL.
"""

from urllib.parse import urlparse, urljoin, urlencode, parse_qs, ParseResult

# Set of domains that are allowed to receive the OAuth callback.
# In a real application this should be configured appropriately.
ALLOWED_CALLBACK_DOMAINS = {
    "example.com",
    "auth.example.org",
}

def assemble_oauth_callback(application_url: str,
                            callback_route: str,
                            token_state: str) -> str:
    """
    Build a fully-qualified OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The root URL of the application (e.g., "https://app.example.com").
    callback_route : str
        The relative or absolute path that handles the OAuth callback
        (e.g., "/auth/callback").
    token_state : str
        A unique string used to preserve state between request and callback.

    Returns
    -------
    str
        The complete callback URL with a ``state`` query parameter.

    Raises
    ------
    ValueError
        If the resolved callback URL points to a domain that is neither
        the same as ``application_url`` nor in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Resolve the callback URL relative to the application root.
    resolved = urljoin(application_url.rstrip('/') + '/', callback_route.lstrip('/'))

    # Parse the resulting URL to examine its components.
    parsed = urlparse(resolved)

    # Extract host part (netloc may contain port).
    host = parsed.hostname
    if not host:
        raise ValueError("Resolved callback URL does not contain a hostname")

    # Determine whether the host is allowed.
    app_host = urlparse(application_url).hostname
    if not app_host:
        raise ValueError("Application URL does not contain a hostname")

    # Normalise to lowercase for comparison.
    host_lc = host.lower()
    app_host_lc = app_host.lower()

    if host_lc != app_host_lc and host_lc not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(f"Callback URL domain '{host}' is not allowed")

    # Append or merge the state query parameter.
    existing_qs = parse_qs(parsed.query, keep_blank_values=True)
    # parse_qs returns lists for each key; we need a single value.
    existing_qs['state'] = [token_state]
    new_query = urlencode(existing_qs, doseq=True)

    # Reconstruct the full URL.
    new_parsed = ParseResult(
        scheme=parsed.scheme,
        netloc=parsed.netloc,
        path=parsed.path,
        params=parsed.params,
        query=new_query,
        fragment=parsed.fragment
    )
    return new_parsed.geturl()