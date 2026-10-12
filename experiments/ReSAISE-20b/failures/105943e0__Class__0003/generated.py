#!/usr/bin/env python3
"""
Utility for building a Single Sign‑On (SSO) redirect URL.
"""

import urllib.parse
from typing import Set

# Define the set of domains that are allowed to be used as callback URLs.
# In a real application this should be populated from configuration
# or environment variables and kept strictly controlled.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "sub.example.org",
    # Add additional domains as required
}


def create_sso_redirect_url(
    login_endpoint: str,
    account_id: str,
    callback_url: str,
) -> str:
    """
    Build a redirect URL for an SSO provider.

    Parameters
    ----------
    login_endpoint : str
        The base URL of the SSO service (e.g. "https://sso.provider.com/auth").
    account_id : str
        The unique identifier for the user to be authenticated.
    callback_url : str
        The URL where the provider should redirect after authentication.

    Returns
    -------
    str
        A fully‑formed URL that can be used to redirect the user to the SSO provider.

    Raises
    ------
    ValueError
        If the callback URL is malformed or its domain is not in ``ALLOWED_RETURN_DOMAINS``.
    """
    # Parse the callback URL to validate and extract its domain
    parsed_callback = urllib.parse.urlparse(callback_url)

    if not parsed_callback.scheme or not parsed_callback.netloc:
        raise ValueError("callback_url must be a valid absolute URL")

    # Normalize domain: strip port and convert to lower case
    callback_domain = parsed_callback.hostname.lower() if parsed_callback.hostname else ""

    # Verify that the domain is in the allowed list
    if callback_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return URL domain '{callback_domain}' is not allowed for SSO redirects."
        )

    # Encode the callback URL so it can be safely included as a query parameter
    encoded_callback = urllib.parse.quote(callback_url, safe="")

    # Build the final redirect URL
    # Ensure we preserve any existing query parameters on the login endpoint.
    parsed_login = urllib.parse.urlparse(login_endpoint)
    # Build query parameters
    query_params = dict(urllib.parse.parse_qsl(parsed_login.query))
    # Add or override the required parameters
    query_params.update(
        {
            "account_id": account_id,
            "redirect_uri": encoded_callback,
        }
    )
    # Reconstruct the URL
    new_query = urllib.parse.urlencode(query_params)
    redirect_url_parts = (
        parsed_login.scheme,
        parsed_login.netloc,
        parsed_login.path,
        parsed_login.params,
        new_query,
        parsed_login.fragment,
    )
    redirect_url = urllib.parse.urlunparse(redirect_url_parts)

    return redirect_url


# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        url = create_sso_redirect_url(
            login_endpoint="https://sso.provider.com/auth",
            account_id="user-12345",
            callback_url="https://example.com/welcome?session=abc",
        )
        print("Redirect URL:", url)
    except ValueError as exc:
        print(f"Error: {exc}")