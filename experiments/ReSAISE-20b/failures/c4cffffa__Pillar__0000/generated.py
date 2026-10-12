#!/usr/bin/env python3
"""
Utility for building a Single Sign-On (SSO) redirect URL.

The function validates the return URL against an allowed domain list,
properly encodes all components, and assembles a secure redirect
link for use in third‑party SSO integrations.
"""

import urllib.parse
from typing import Set

# Example set of domains allowed to receive the redirect back.
ALLOWED_RETURN_DOMAINS: Set[str] = {"example.com", "trustedpartner.org"}

def build_sso_redirect_link(
    sso_service_url: str,
    user_identifier: str,
    redirect_back_url: str
) -> str:
    """
    Build a secure SSO redirect URL.

    Parameters
    ----------
    sso_service_url : str
        Base URL of the SSO provider (e.g., "https://sso.example.com/login").
    user_identifier : str
        Unique identifier for the user (e.g., UUID, email).
    redirect_back_url : str
        URL to return to after successful SSO authentication.

    Returns
    -------
    str
        Fully formed redirect URL with query parameters properly encoded.

    Raises
    ------
    ValueError
        If the domain of ``redirect_back_url`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate that the return URL's domain is allowed
    parsed_return = urllib.parse.urlparse(redirect_back_url)
    if not parsed_return.scheme or not parsed_return.netloc:
        raise ValueError("redirect_back_url must be a valid absolute URL")

    # Extract hostname and normalize it (lowercase)
    host = parsed_return.hostname.lower() if parsed_return.hostname else ""
    if host not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Return domain '{host}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_RETURN_DOMAINS)}"
        )

    # Parse the SSO service URL to ensure it's valid and extract components
    parsed_sso = urllib.parse.urlparse(sso_service_url)
    if not parsed_sso.scheme or not parsed_sso.netloc:
        raise ValueError("sso_service_url must be a valid absolute URL")

    # Construct query parameters
    params = {
        "user_id": user_identifier,
        "redirect_uri": redirect_back_url
    }

    # Encode query parameters safely
    encoded_params = urllib.parse.urlencode(params, safe="")

    # Assemble the final URL
    # Preserve any existing query parameters in the SSO service URL
    if parsed_sso.query:
        # Merge existing and new parameters
        merged_query = urllib.parse.urlencode(
            dict(urllib.parse.parse_qsl(parsed_sso.query), **params),
            safe=""
        )
    else:
        merged_query = encoded_params

    # Rebuild the URL with the new query string
    final_url_parts = parsed_sso._replace(query=merged_query)
    final_url = urllib.parse.urlunparse(final_url_parts)

    return final_url


# Example usage
if __name__ == "__main__":
    try:
        link = build_sso_redirect_link(
            sso_service_url="https://sso.example.com/login",
            user_identifier="user-12345",
            redirect_back_url="https://example.com/dashboard"
        )
        print("SSO Redirect URL:", link)
    except ValueError as e:
        print("Error building SSO redirect link:", e)