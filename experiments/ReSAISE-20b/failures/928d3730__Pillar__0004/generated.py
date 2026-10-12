#!/usr/bin/env python3
"""
Utility to generate a secure OAuth callback URL.

The function validates that the resulting callback domain is either
the same as the application's host or belongs to a whitelist of allowed
domains. It also attaches a state parameter derived from the supplied
session identifier.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Set


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Define the set of domains that are explicitly allowed for OAuth callbacks.
# This should be populated with trusted third‑party domains or left empty
# if only same‑origin callbacks are permitted.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    # Example entries:
    # "auth.example.com",
    # "oauth.partner.org",
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a fully qualified OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The root URL of the application (e.g., "https://app.example.com").
    path_callback : str
        The relative endpoint that will handle the OAuth callback
        (e.g., "/auth/callback").
    session_id : str
        A unique identifier that will be added as the `state` query
        parameter to protect against CSRF attacks.

    Returns
    -------
    str
        A fully assembled, validated OAuth callback URL containing the
        `state` parameter.

    Raises
    ------
    ValueError
        If the callback URL's domain is neither the same as the host
        nor in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # --------------------------------------------------------------------- #
    # Normalise input
    # --------------------------------------------------------------------- #

    if not host_url:
        raise ValueError("host_url must be a non-empty string")
    if not path_callback.startswith("/"):
        raise ValueError("path_callback must start with '/'")

    # Resolve the absolute callback URL
    base_parsed = urllib.parse.urlparse(host_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid host_url: {host_url!r}")

    # Construct the absolute callback URL
    joined = urllib.parse.urljoin(host_url, path_callback)
    callback_parsed = urllib.parse.urlparse(joined)

    # --------------------------------------------------------------------- #
    # Security checks
    # --------------------------------------------------------------------- #

    callback_domain = callback_parsed.netloc.lower()
    host_domain = base_parsed.netloc.lower()

    # Ensure the callback domain is either the same as the host or explicitly allowed
    if callback_domain != host_domain and callback_domain not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(
            f"Callback domain '{callback_domain}' is not allowed. "
            f"Must be the same as host ('{host_domain}') or in ALLOWED_CALLBACK_DOMAINS."
        )

    # --------------------------------------------------------------------- #
    # Append the state parameter
    # --------------------------------------------------------------------- #

    query = urllib.parse.parse_qs(callback_parsed.query, keep_blank_values=True)
    # Avoid overriding existing state values; use a list to preserve semantics
    query.setdefault("state", []).append(session_id)

    # Rebuild the URL with the new query string
    new_query = urllib.parse.urlencode(query, doseq=True)
    final_url_parts = (
        callback_parsed.scheme,
        callback_parsed.netloc,
        callback_parsed.path,
        callback_parsed.params,
        new_query,
        callback_parsed.fragment,
    )
    final_url = urllib.parse.urlunparse(final_url_parts)

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Example values
    host = "https://app.example.com"
    callback_path = "/auth/callback"
    session = "abc123XYZ"

    try:
        url = generate_oauth_url(host, callback_path, session)
        print(f"Generated OAuth URL: {url}")
    except ValueError as exc:
        print(f"Error generating OAuth URL: {exc}")