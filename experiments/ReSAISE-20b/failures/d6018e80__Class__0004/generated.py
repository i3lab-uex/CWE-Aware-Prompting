#!/usr/bin/env python3
"""
Create a secure Single Sign-On redirect URL.

The function validates the return URL against an allow‑list of domains
to mitigate CWE‑610 (Externally Controlled Reference to a Resource in Another Sphere)
and then builds the final SSO URL with properly encoded query parameters.
"""

import urllib.parse
from typing import Set

# Example allow‑list of domains. Replace or extend as needed.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "app.example.org",
    "login.myservice.net",
}

def _extract_domain(url: str) -> str:
    """
    Extract the domain (netloc) from a URL.
    Handles URLs with or without scheme.
    """
    parsed = urllib.parse.urlparse(url if "://" in url else f"https://{url}")
    # Remove port if present
    return parsed.hostname or ""

def create_sso_redirect_url(sso_url: str, uid: str, redirect_url: str) -> str:
    """
    Build a SSO redirect URL.

    Parameters
    ----------
    sso_url : str
        Base URL of the SSO service (may already contain query parameters).
    uid : str
        Unique identifier for the user.
    redirect_url : str
        URL to return to after authentication.

    Returns
    -------
    str
        Fully constructed SSO redirect URL with query parameters.

    Raises
    ------
    ValueError
        If the domain of `redirect_url` is not in ALLOWED_RETURN_DOMAINS.
    """
    # Validate the return URL domain
    domain = _extract_domain(redirect_url)
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed.")

    # Encode the parameters
    query_params = {
        "user": uid,
        "return_url": redirect_url,  # Will be percent‑encoded by urlencode
    }
    encoded_params = urllib.parse.urlencode(query_params, safe=":/?#[]@!$&'()*+,;=")

    # Parse the base SSO URL to preserve existing components
    parsed_sso = urllib.parse.urlparse(sso_url)
    # Merge existing query parameters with new ones
    if parsed_sso.query:
        merged_query = f"{parsed_sso.query}&{encoded_params}"
    else:
        merged_query = encoded_params

    # Reconstruct the full URL
    final_url_parts = parsed_sso._replace(query=merged_query)
    return urllib.parse.urlunparse(final_url_parts)

# Example usage
if __name__ == "__main__":
    try:
        url = create_sso_redirect_url(
            sso_url="https://sso.example.com/auth",
            uid="user123",
            redirect_url="https://app.example.org/dashboard"
        )
        print(url)
    except ValueError as e:
        print(f"Error: {e}")