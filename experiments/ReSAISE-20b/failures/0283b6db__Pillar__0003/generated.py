#!/usr/bin/env python3
"""
Utility for generating a secure SSO redirect URL.
"""

from urllib.parse import urlparse, urlencode, urljoin

# Domains that are allowed for the return URL. Adjust as needed.
ALLOWED_RETURN_DOMAINS = {"example.com", "app.example.org"}


def _extract_domain(url: str) -> str:
    """
    Extract the network location (domain) from a URL.
    Handles URLs with or without scheme.
    """
    parsed = urlparse(url if "://" in url else f"https://{url}")
    return parsed.hostname or ""


def generate_sso_redirect(sso_endpoint: str, user_id: str, return_url: str) -> str:
    """
    Generate a Single Sign-On (SSO) redirect URL.

    Parameters
    ----------
    sso_endpoint : str
        The base endpoint of the SSO service.
    user_id : str
        Unique identifier for the user (e.g., a UUID).
    return_url : str
        URL to redirect back to after successful authentication.

    Returns
    -------
    str
        Fully-qualified SSO redirect URL with query parameters.

    Raises
    ------
    ValueError
        If `return_url` does not belong to an allowed domain.
    """
    # Validate return URL domain
    domain = _extract_domain(return_url)
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(f"Return URL domain '{domain}' is not allowed")

    # Build query parameters
    params = {
        "user_id": user_id,
        "return_url": return_url,
    }
    query_string = urlencode(params, safe=":/?&")  # keep URL-safe characters

    # Combine the SSO endpoint with the query string
    sso_url = urljoin(sso_endpoint.rstrip("/") + "/", f"?{query_string}")

    return sso_url