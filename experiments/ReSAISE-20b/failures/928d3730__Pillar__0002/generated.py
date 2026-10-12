#!/usr/bin/env python3
"""
Utility for generating a secure OAuth callback URL.

The function validates that the resulting URL's domain is either
within an allowed set or matches the application's own host domain.
"""

from urllib.parse import urlparse, urljoin, urlencode
from typing import Set

# Predefined set of domains that are considered safe for callbacks.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    # Add more trusted domains here
}

def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a fully-qualified OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The root URL of the application (e.g., "https://app.example.com").
    path_callback : str
        The endpoint for the OAuth callback handler (e.g., "/auth/callback").
    session_id : str
        A unique identifier to maintain the integrity of the OAuth exchange.

    Returns
    -------
    str
        A fully assembled, validated callback URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS and does not match
        the host domain.
    """
    # Ensure we have a proper base URL (scheme and netloc)
    parsed_host = urlparse(host_url)
    if not parsed_host.scheme or not parsed_host.netloc:
        raise ValueError(f"Invalid host_url: {host_url!r}")

    # Construct the full callback URL
    base_callback = urljoin(host_url, path_callback)

    # Append the state parameter securely
    query_params = {"state": session_id}
    callback_with_state = f"{base_callback}?{urlencode(query_params)}"

    # Validate domain
    parsed_callback = urlparse(callback_with_state)
    callback_domain = parsed_callback.netloc.lower()

    host_domain = parsed_host.netloc.lower()
    if callback_domain not in ALLOWED_CALLBACK_DOMAINS and callback_domain != host_domain:
        raise ValueError(
            f"Disallowed callback domain: {callback_domain!r}. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)} or host domain '{host_domain}'."
        )

    return callback_with_state

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     url = generate_oauth_url(
#         host_url="https://app.example.com",
#         path_callback="/oauth/callback",
#         session_id="abc123def456"
#     )
#     print(url)