#!/usr/bin/env python3
"""
Utility to build a secure SSO redirect URL.

The function validates that the supplied `redirect_url` belongs to an
approved domain, then constructs a full redirect URL for the SSO service.
"""

from __future__ import annotations

import urllib.parse
from typing import Set


# --------------------------------------------------------------------------- #
# Configuration – domains that are allowed to be used as a return URL.
# --------------------------------------------------------------------------- #
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "sub.example.com",
    # Add additional trusted domains here
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _extract_domain(url: str) -> str:
    """
    Extract the hostname from a URL. Raises ValueError if parsing fails.
    """
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError(f"Invalid URL: '{url}' – no hostname found.")
    return hostname.lower()


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def build_sso_redirect(auth_endpoint: str, uid: str, redirect_url: str) -> str:
    """
    Construct a full SSO redirect URL.

    Parameters
    ----------
    auth_endpoint : str
        The base URL of the SSO service endpoint.
    uid : str
        Unique identifier for the user to be authenticated.
    redirect_url : str
        The URL to which the user should be returned after authentication.

    Returns
    -------
    str
        The fully-qualified redirect URL for the SSO process.

    Raises
    ------
    ValueError
        If the `redirect_url` domain is not in :data:`ALLOWED_RETURN_DOMAINS`,
        or if any URL parsing fails.
    """
    # Validate the redirect URL domain
    target_domain = _extract_domain(redirect_url)
    if target_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{target_domain}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_RETURN_DOMAINS)}"
        )

    # Ensure the auth_endpoint is absolute and has no fragment
    parsed_auth = urllib.parse.urlparse(auth_endpoint)
    if not parsed_auth.scheme or not parsed_auth.netloc:
        raise ValueError(f"Invalid auth_endpoint URL: '{auth_endpoint}'")

    # Build query parameters
    query_params = {
        "uid": uid,
        "redirect_url": redirect_url,  # The SSO service should handle decoding
    }

    # Construct the final URL
    new_query = urllib.parse.urlencode(query_params)
    sso_url_parts = (
        parsed_auth.scheme,
        parsed_auth.netloc,
        parsed_auth.path or "",
        parsed_auth.params,
        new_query,
        "",  # fragment
    )
    final_url = urllib.parse.urlunparse(sso_url_parts)

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (for debugging / manual testing)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        result = build_sso_redirect(
            auth_endpoint="https://sso.example.com/auth",
            uid="user-12345",
            redirect_url="https://app.example.com/welcome?token=abc",
        )
        print("SSO redirect URL:")
        print(result)
    except ValueError as e:
        print(f"Error: {e}")