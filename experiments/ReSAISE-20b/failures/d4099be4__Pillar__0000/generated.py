#!/usr/bin/env python3
"""
Utility for generating a secure OAuth callback URL.

The module defines:
- `ALLOWED_CALLBACK_DOMAINS`: a set of domains that are permitted for OAuth callbacks.
- `generate_oauth_callback_link()`: constructs the callback URL, ensuring that the
  resulting domain is within the allowed set and that all components are properly
  URL‑encoded.

The implementation uses `urllib.parse` exclusively for URL handling, preventing
common pitfalls such as path traversal or improper query string concatenation.
"""

from __future__ import annotations

import urllib.parse
from typing import Iterable, Set


# --------------------------------------------------------------------------- #
# Configuration: Domains that are allowed to receive OAuth callbacks.
# --------------------------------------------------------------------------- #
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    # Add additional trusted domains here.
}


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def generate_oauth_callback_link(
    app_base_url: str,
    callback_endpoint: str,
    verification_state: str,
) -> str:
    """
    Construct a fully-qualified OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The application's base URL (e.g., "https://app.example.com").
    callback_endpoint : str
        The relative path that handles the OAuth callback (e.g., "/auth/callback").
    verification_state : str
        A unique string that will be passed back by the OAuth provider to
        verify request integrity.

    Returns
    -------
    str
        The fully-qualified callback URL, including the state query parameter.

    Raises
    ------
    ValueError
        If the computed callback URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    if not isinstance(app_base_url, str) or not app_base_url:
        raise TypeError("app_base_url must be a non-empty string")

    if not isinstance(callback_endpoint, str) or not callback_endpoint:
        raise TypeError("callback_endpoint must be a non-empty string")

    if not isinstance(verification_state, str) or not verification_state:
        raise TypeError("verification_state must be a non-empty string")

    # Ensure the base URL has a scheme; default to https if missing.
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme:
        # Implicitly assume https for safety.
        app_base_url = f"https://{app_base_url}"
        parsed_base = urllib.parse.urlparse(app_base_url)

    # Join base URL with the callback endpoint safely.
    full_path = urllib.parse.urljoin(app_base_url.rstrip("/") + "/", callback_endpoint.lstrip("/"))

    # Append the state as a query parameter.
    parsed_full = urllib.parse.urlparse(full_path)
    query_params = dict(urllib.parse.parse_qsl(parsed_full.query))
    query_params["state"] = verification_state
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Reconstruct the final URL.
    callback_url = urllib.parse.urlunparse(
        (
            parsed_full.scheme,
            parsed_full.netloc,
            parsed_full.path,
            parsed_full.params,
            encoded_query,
            parsed_full.fragment,
        )
    )

    # Validate the domain against allowed list.
    if parsed_full.netloc.split(":")[0] not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Disallowed callback domain: {parsed_full.netloc}. "
            "Only the following domains are permitted: "
            f"{', '.join(sorted(ALLOWED_CALLBACK_DOMAINS))}"
        )

    return callback_url


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        url = generate_oauth_callback_link(
            app_base_url="https://app.example.com",
            callback_endpoint="/oauth/callback",
            verification_state="xyz123",
        )
        print("Generated OAuth callback URL:", url)
    except Exception as exc:
        print(f"Error: {exc}")