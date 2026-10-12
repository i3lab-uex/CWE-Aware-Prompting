#!/usr/bin/env python3
"""
Utility to construct a secure SSO redirect URL.

The function validates that the supplied return URL belongs to an
approved domain before embedding it into a redirect query string.
"""

from __future__ import annotations

import urllib.parse
from typing import Set


# ----------------------------------------------------------------------
# Allowed domains for the return URL.
# In a real application, populate this set with your own whitelisted domains.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "sub.example.org",
}

# ----------------------------------------------------------------------
def create_sso_redirect_url(
    sso_url: str, uid: str, redirect_url: str
) -> str:
    """
    Construct a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the third‑party SSO service (must be a valid absolute URL).
    uid : str
        Unique identifier of the user.
    redirect_url : str
        URL to which the SSO provider should return after authentication.

    Returns
    -------
    str
        Fully formed redirect URL ready to be sent to the user.

    Raises
    ------
    ValueError
        If the return URL's domain is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the base SSO URL
    parsed_sso = urllib.parse.urlparse(sso_url)
    if not (parsed_sso.scheme and parsed_sso.netloc):
        raise ValueError(f"Invalid SSO URL: {sso_url!r}")

    # Validate the redirect URL
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    if not (parsed_redirect.scheme and parsed_redirect.netloc):
        raise ValueError(f"Invalid redirect URL: {redirect_url!r}")

    # Extract the hostname and normalize it (lowercase, strip port)
    hostname = parsed_redirect.hostname
    if hostname is None:
        raise ValueError(f"Redirect URL must contain a hostname: {redirect_url!r}")

    # Compare against allowed domains
    if not any(hostname == domain or hostname.endswith(f".{domain}") for domain in ALLOWED_RETURN_DOMAINS):
        raise ValueError(
            f"Return URL domain {hostname!r} is not permitted"
        )

    # Build the query string for the SSO service
    sso_query = {
        "uid": uid,
        # The redirect URL must be encoded so that the SSO provider can parse it.
        "return_url": redirect_url,
    }
    encoded_query = urllib.parse.urlencode(sso_query, doseq=True)

    # Construct the final URL
    sso_parts = list(parsed_sso)
    # Preserve any existing query parameters by merging them
    if parsed_sso.query:
        merged_query = f"{parsed_sso.query}&{encoded_query}"
    else:
        merged_query = encoded_query
    sso_parts[4] = merged_query  # index 4 is the query component

    final_url = urllib.parse.urlunparse(sso_parts)
    return final_url


# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Example usage
    try:
        url = create_sso_redirect_url(
            sso_url="https://sso.example.com/auth",
            uid="user-12345",
            redirect_url="https://example.com/welcome?session=abc",
        )
        print("Redirect URL:", url)
    except ValueError as exc:
        print(f"Error: {exc}")