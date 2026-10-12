#!/usr/bin/env python3
"""
Utility to safely assemble an OAuth callback URL.

The function validates that the resulting callback URL belongs either
to the same host as the application or to one of a pre‑approved set
of domains.  This protects against open‑redirect attacks (CWE‑601).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Set


# A set of domains that are explicitly allowed for OAuth callbacks.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "auth.example.com",
    "oauth.partner.com",
}


def _normalize_domain(host: str) -> str:
    """
    Normalise a host name for comparison.
    Strips port numbers and converts to lowercase.

    Parameters
    ----------
    host : str
        The hostname extracted from a URL (may contain a port).

    Returns
    -------
    str
        Normalised hostname.
    """
    if not host:
        return ""
    # Split off port number if present
    hostname = host.split(":")[0].lower()
    return hostname


def assemble_oauth_callback(
    application_url: str,
    callback_route: str,
    token_state: str,
) -> str:
    """
    Build a fully‑qualified OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The base URL of the application (e.g. "https://app.example.com").
    callback_route : str
        The path or relative URL where the OAuth provider will redirect.
        Must be a safe, relative path (e.g. "/auth/callback").
    token_state : str
        A unique, opaque identifier used to maintain state between the
        request and callback.  It is appended as a query parameter.

    Returns
    -------
    str
        A fully qualified, validated callback URL.

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not allowed.
    """
    # ------------------------------------------------------------------
    # 1. Validate the callback_route – it must be a relative path.
    # ------------------------------------------------------------------
    parsed_callback = urllib.parse.urlparse(callback_route)
    if parsed_callback.scheme or parsed_callback.netloc:
        raise ValueError(
            "callback_route must be a relative path, not an absolute URL"
        )
    if not parsed_callback.path.startswith("/"):
        raise ValueError(
            "callback_route must start with a leading slash (e.g. '/auth/callback')"
        )

    # ------------------------------------------------------------------
    # 2. Combine application_url and callback_route.
    # ------------------------------------------------------------------
    base_parsed = urllib.parse.urlparse(application_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("application_url must be a valid absolute URL")

    # urljoin handles trailing slashes correctly.
    combined = urllib.parse.urljoin(application_url, callback_route)

    # ------------------------------------------------------------------
    # 3. Append the state parameter safely.
    # ------------------------------------------------------------------
    query = urllib.parse.urlencode({"state": token_state})
    if parsed_callback.query:
        # Preserve any existing query parameters.
        query = f"{parsed_callback.query}&{query}"
    callback_url = urllib.parse.urlunparse(
        (
            base_parsed.scheme,
            base_parsed.netloc,
            urllib.parse.urljoin(base_parsed.path, parsed_callback.path),
            "",  # params
            query,
            "",  # fragment
        )
    )

    # ------------------------------------------------------------------
    # 4. Validate the domain.
    # ------------------------------------------------------------------
    callback_parsed = urllib.parse.urlparse(callback_url)
    callback_domain = _normalize_domain(callback_parsed.hostname)

    app_domain = _normalize_domain(base_parsed.hostname)
    if callback_domain != app_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Disallowed callback domain: {callback_domain}. "
            "Only the application host or ALLOWED_CALLBACK_DOMAINS are permitted."
        )

    return callback_url


# ------------------------------------------------------------------
# Example usage (uncomment for quick test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     url = assemble_oauth_callback(
#         application_url="https://app.example.com",
#         callback_route="/oauth/callback",
#         token_state="abc123"
#     )
#     print(url)