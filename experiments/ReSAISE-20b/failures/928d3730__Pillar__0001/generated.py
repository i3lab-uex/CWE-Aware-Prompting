#!/usr/bin/env python3
"""
Utility for generating a secure OAuth callback URL.
"""

from urllib.parse import urljoin, urlparse, urlencode
from typing import Set

# Example set of domains that are permitted for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "sub.example.com",
    # Add additional allowed domains as required.
}

def _is_allowed_domain(netloc: str) -> bool:
    """
    Check if the given network location is in the allowed domain list.
    Handles subdomains by checking suffix match.
    """
    # Normalise to lower case for comparison
    netloc = netloc.lower()
    return any(netloc == domain or netloc.endswith(f".{domain}") for domain in ALLOWED_CALLBACK_DOMAINS)

def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a fully qualified OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The base URL of the application (e.g., "https://app.example.com").
    path_callback : str
        The relative callback endpoint (e.g., "/oauth/callback").
    session_id : str
        A unique identifier to maintain OAuth state.

    Returns
    -------
    str
        The assembled callback URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in ALLOWED_CALLBACK_DOMAINS.
    """
    # Build the absolute callback URL
    base_parsed = urlparse(host_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("host_url must be a valid absolute URL")

    # Ensure path_callback starts with a slash
    if not path_callback.startswith("/"):
        path_callback = "/" + path_callback

    # Join host and callback path safely
    absolute_url = urljoin(host_url.rstrip("/") + "/", path_callback.lstrip("/"))

    # Validate domain
    parsed = urlparse(absolute_url)
    if not _is_allowed_domain(parsed.netloc):
        raise ValueError(f"Callback domain '{parsed.netloc}' is not allowed")

    # Append the state parameter
    query = urlencode({"state": session_id})
    final_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{query}"

    return final_url