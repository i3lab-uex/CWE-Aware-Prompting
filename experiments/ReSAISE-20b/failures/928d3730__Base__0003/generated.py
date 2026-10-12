#!/usr/bin/env python3
"""
Utility to generate a secure OAuth callback URL.

The implementation protects against open‑redirect vulnerabilities by ensuring that
the final callback URL either points to the same host as the application or is
explicitly whitelisted in ALLOWED_CALLBACK_DOMAINS.
"""

from __future__ import annotations

import urllib.parse
from typing import Set

# Example whitelist – in a real application this should be populated from config.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.myapp.io"}

def generate_oauth_url(host_url: str, path_callback: str, session_id: str) -> str:
    """
    Construct a fully qualified OAuth callback URL.

    Parameters
    ----------
    host_url : str
        The base URL of the application (e.g., "https://myapp.com").
    path_callback : str
        The relative or absolute path for the OAuth callback handler
        (e.g., "/auth/callback" or "https://evil.com/").
    session_id : str
        A unique identifier to be passed as the `state` query parameter.

    Returns
    -------
    str
        The complete callback URL, including the `state` query parameter.

    Raises
    ------
    ValueError
        If the resolved callback URL points to a domain that is not
        whitelisted or does not match the host's domain.
    """
    if not host_url:
        raise ValueError("host_url must be a non-empty string")
    if not path_callback:
        raise ValueError("path_callback must be a non-empty string")
    if not session_id:
        raise ValueError("session_id must be a non-empty string")

    # Parse the host URL to ensure it has a scheme and netloc
    parsed_host = urllib.parse.urlparse(host_url)
    if not parsed_host.scheme or not parsed_host.netloc:
        raise ValueError(f"Invalid host_url: {host_url!r}")

    # Resolve the callback URL relative to the host
    resolved = urllib.parse.urljoin(host_url, path_callback)

    # Parse the resolved URL to extract its domain
    parsed_resolved = urllib.parse.urlparse(resolved)
    callback_domain = parsed_resolved.hostname
    if not callback_domain:
        raise ValueError(f"Unable to determine domain from callback URL: {resolved!r}")

    # Ensure the callback domain is either the same as the host or in the whitelist
    if (callback_domain.lower() != parsed_host.hostname.lower()
            and callback_domain.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}):
        raise ValueError(
            f"Callback domain '{callback_domain}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    # Append the state parameter securely
    query = urllib.parse.parse_qs(parsed_resolved.query, keep_blank_values=True)
    query["state"] = [session_id]
    new_query = urllib.parse.urlencode(query, doseq=True)

    # Reconstruct the URL with the new query string
    final_url = urllib.parse.urlunparse(
        parsed_resolved._replace(query=new_query)
    )
    return final_url