#!/usr/bin/env python3
"""
OAuth callback URL generator.

This module defines a single function `create_oauth_callback_url` that
builds an OAuth callback URL by combining a base application URL with a
specific callback path and appending a security state parameter.
The function validates that the resulting URL belongs to an allowed
domain, preventing open redirect vulnerabilities.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Set


# --------------------------------------------------------------------------- #
# Configuration: allowed callback domains.  Update this set as needed.
# --------------------------------------------------------------------------- #
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    # Add any additional domains that your application is allowed to use
}


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def create_oauth_callback_url(
    base_url: str,
    callback_path: str,
    state: str,
) -> str:
    """
    Build a fully-qualified OAuth callback URL.

    Parameters
    ----------
    base_url : str
        The application's base URL, e.g. "https://myapp.example.com".
    callback_path : str
        The path component that will handle the OAuth callback,
        e.g. "/auth/oauth/callback".
    state : str
        A cryptographically random string used to mitigate CSRF attacks.

    Returns
    -------
    str
        The complete OAuth callback URL with the state query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL resolves to a domain that is not in
        :data:`ALLOWED_CALLBACK_DOMAINS`.

    Notes
    -----
    - The function normalises the base URL and callback path to avoid
      double slashes or missing separators.
    - The `state` value is URL‑encoded to ensure it is safe as a query
      component.
    - Domain validation uses the host part of the parsed URL; it does not
      check sub‑domains unless explicitly listed in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    if not base_url:
        raise ValueError("base_url must be a non-empty string")
    if not callback_path:
        raise ValueError("callback_path must be a non-empty string")
    if not state:
        raise ValueError("state must be a non-empty string")

    # Normalise base URL: ensure it ends with a single slash
    normalized_base = base_url.rstrip("/") + "/"

    # Use urllib.parse.urljoin to combine the base with the callback path
    full_path = urllib.parse.urljoin(normalized_base, callback_path.lstrip("/"))

    # Append the state query parameter
    parsed = urllib.parse.urlparse(full_path)
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    query_params["state"] = state
    encoded_query = urllib.parse.urlencode(query_params)

    # Reconstruct the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            encoded_query,
            parsed.fragment,
        )
    )

    # Validate that the host is in the allowed set
    hostname = urllib.parse.urlparse(final_url).hostname
    if hostname is None or hostname.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Disallowed callback domain: {hostname!r}. "
            f"Allowed domains are: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example: generate a callback URL for the OAuth flow
    try:
        url = create_oauth_callback_url(
            base_url="https://myapp.example.com",
            callback_path="/oauth/callback",
            state="1234567890abcdef",
        )
        print("Generated callback URL:", url)
    except ValueError as exc:
        print("Error:", exc)