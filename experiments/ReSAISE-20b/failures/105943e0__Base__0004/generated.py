#!/usr/bin/env python3
"""
Utility to construct a secure SSO redirect URL.

The function validates that the callback URL belongs to an allowed domain
before embedding it in the redirect.  This prevents open‑redirect attacks
(CWE‑601) by ensuring that users are only sent back to trusted destinations.
"""

from urllib.parse import urlparse, urlencode, urlunparse
from typing import Set

# Domains that are considered safe for the return URL.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "app.example.org",
    # Add more domains as needed.
}

def create_sso_redirect_url(login_endpoint: str,
                            account_id: str,
                            callback_url: str) -> str:
    """
    Build a full SSO redirect URL.

    Parameters
    ----------
    login_endpoint : str
        Base URL of the SSO service endpoint.
    account_id : str
        Unique identifier for the user (will be passed as a query param).
    callback_url : str
        URL to return the user after authentication.

    Returns
    -------
    str
        Fully constructed redirect URL.

    Raises
    ------
    ValueError
        If the callback URL's domain is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Parse the callback URL and verify its domain.
    parsed_cb = urlparse(callback_url)
    if not parsed_cb.scheme in {"http", "https"}:
        raise ValueError("Callback URL must use http or https scheme")

    domain = parsed_cb.hostname
    if not domain:
        raise ValueError("Callback URL must contain a hostname")

    # Normalize the domain (lowercase) for comparison.
    if domain.lower() not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Domain '{domain}' is not allowed for callback URLs")

    # Construct the query parameters.
    query_params = {
        "account_id": account_id,
        "return_url": callback_url,  # will be percent‑encoded by urlencode
    }
    encoded_query = urlencode(query_params)

    # Build the final redirect URL.
    parsed_login = urlparse(login_endpoint)
    if not parsed_login.scheme or not parsed_login.netloc:
        raise ValueError("Invalid login endpoint URL")

    # Preserve any existing query parameters in the login endpoint.
    new_query = encoded_query
    if parsed_login.query:
        # Append to existing query string.
        new_query = f"{parsed_login.query}&{encoded_query}"

    redirect_url = urlunparse((
        parsed_login.scheme,
        parsed_login.netloc,
        parsed_login.path,
        parsed_login.params,
        new_query,
        parsed_login.fragment,
    ))

    return redirect_url