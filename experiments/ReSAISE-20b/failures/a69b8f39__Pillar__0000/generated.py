#!/usr/bin/env python3
"""
Utility to build a Single Sign-On (SSO) redirect URL.

The function validates the return URL against an allowed set of domains
to guard against open‑redirect attacks (CWE-664).
"""

from __future__ import annotations

import urllib.parse
from typing import Set, Dict

# Example set of allowed domains.  Replace with your own configuration.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "app.example.org",
}

def _validate_return_domain(return_url: str) -> None:
    """
    Ensure the return URL's domain is within ALLOWED_RETURN_DOMAINS.

    Raises:
        ValueError: If the domain is not allowed.
    """
    parsed = urllib.parse.urlparse(return_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid return URL: {return_url}")

    # Extract the hostname (excluding port)
    host = parsed.hostname
    if host is None:
        raise ValueError(f"Unable to determine hostname for return URL: {return_url}")

    # Compare against allowed domains
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{host}' is not permitted")

def build_sso_redirect_url(sso_service: str, user_ref: str, back_url: str) -> str:
    """
    Construct an SSO redirect URL that includes user reference and a safe
    return URL.

    Parameters:
        sso_service (str): Base URL of the SSO service.
        user_ref (str): Unique identifier for the user.
        back_url (str): URL to redirect back after SSO.

    Returns:
        str: Fully formed SSO redirect URL.

    Raises:
        ValueError: If the back_url domain is not in ALLOWED_RETURN_DOMAINS.
    """
    # Validate return URL
    _validate_return_domain(back_url)

    # Parse the base SSO service URL to handle existing query parameters
    parsed_sso = urllib.parse.urlparse(sso_service)

    # Prepare new query parameters
    new_params: Dict[str, str] = {
        "user_ref": user_ref,
        "return_url": back_url,
    }

    # Merge with any existing query parameters
    existing_params = urllib.parse.parse_qs(parsed_sso.query, keep_blank_values=True)
    # parse_qs returns lists; flatten for single values
    existing_params = {k: v[0] if v else "" for k, v in existing_params.items()}
    merged_params = {**existing_params, **new_params}

    # Build the new query string
    encoded_query = urllib.parse.urlencode(merged_params, doseq=False)

    # Reconstruct the full URL
    sso_redirect = urllib.parse.urlunparse(
        parsed_sso._replace(query=encoded_query)
    )

    return sso_redirect

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    try:
        url = build_sso_redirect_url(
            sso_service="https://sso.example.com/login",
            user_ref="user123",
            back_url="https://app.example.org/dashboard"
        )
        print(url)
    except ValueError as e:
        print(f"Error: {e}")