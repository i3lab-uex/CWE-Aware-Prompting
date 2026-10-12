#!/usr/bin/env python3
"""
Utility for generating a secure SSO redirect URL.

The implementation validates that the supplied callback URL is within an
approved domain list before constructing the final redirect link.  It uses
`urllib.parse` to safely encode query parameters and avoid URL injection
issues.

Author: ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Set


# A set of domains that are allowed as callback URLs.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    # Add more allowed domains as needed.
}


def _validate_return_url(callback_url: str) -> None:
    """
    Ensure that the callback URL's domain is in ALLOWED_RETURN_DOMAINS.

    Raises:
        ValueError: If the domain is not allowed.
    """
    parsed = urllib.parse.urlparse(callback_url)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Callback URL must contain a valid hostname.")

    # Allow subdomains of approved domains
    for allowed in ALLOWED_RETURN_DOMAINS:
        if hostname == allowed or hostname.endswith(f".{allowed}"):
            return

    raise ValueError(
        f"Callback URL domain '{hostname}' is not in the list of allowed domains."
    )


def create_sso_redirect_url(
    login_endpoint: str, account_id: str, callback_url: str
) -> str:
    """
    Build a secure redirect URL for an SSO authentication flow.

    Parameters
    ----------
    login_endpoint : str
        The base URL of the SSO provider's login endpoint.
    account_id : str
        Unique identifier for the user (e.g., user ID or username).
    callback_url : str
        The URL to redirect the user back to after authentication.

    Returns
    -------
    str
        A fully-formed URL that can be used to redirect the user.

    Raises
    ------
    ValueError
        If the callback URL's domain is not in `ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the callback URL first
    _validate_return_url(callback_url)

    # Parse the login endpoint to preserve any existing query parameters
    parsed_login = urllib.parse.urlparse(login_endpoint)
    login_query = dict(urllib.parse.parse_qsl(parsed_login.query))

    # Add or overwrite the required SSO parameters
    login_query.update(
        {
            "account_id": account_id,
            "callback_url": callback_url,
        }
    )

    # Reconstruct the login URL with updated query parameters
    new_query = urllib.parse.urlencode(login_query, doseq=True)
    final_url_parts = parsed_login._replace(query=new_query)

    return urllib.parse.urlunparse(final_url_parts)


# Example usage (for demonstration only; remove or guard in production)
if __name__ == "__main__":
    try:
        redirect = create_sso_redirect_url(
            "https://sso.example.com/login",
            account_id="user123",
            callback_url="https://app.example.com/welcome?foo=bar",
        )
        print("Redirect URL:", redirect)
    except ValueError as exc:
        print(f"Invalid callback URL: {exc}")