#!/usr/bin/env python3
"""
Utility to build a secure OAuth redirect URL.

The function validates that the callback domain is either:
* exactly the same as the main application domain, or
* present in a pre‑defined whitelist (ALLOWED_CALLBACK_DOMAINS).

If the domain fails validation, a ValueError is raised.
"""

from __future__ import annotations

import urllib.parse
from typing import Iterable, Set


# Example whitelist – replace with your own allowed domains.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.myapp.org"}


def _extract_domain(url: str) -> str:
    """
    Return the network location part of a URL in lower case.
    Raises ValueError if the URL is malformed or has no netloc.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {url!r}")
    return parsed.hostname.lower()


def build_oauth_redirect_url(
    main_url: str,
    redirect_endpoint: str,
    session_state: str,
) -> str:
    """
    Construct a fully qualified OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The root URL of the application (e.g. "https://myapp.com").
    redirect_endpoint : str
        The path or endpoint that handles the OAuth callback
        (e.g. "/auth/callback").
    session_state : str
        A unique token that will be sent back as a query parameter
        to protect against CSRF attacks.

    Returns
    -------
    str
        The fully assembled, validated callback URL.

    Raises
    ------
    ValueError
        If the resulting domain is not allowed.
    """
    # Resolve the absolute callback URL from the base and endpoint
    callback_url = urllib.parse.urljoin(main_url.rstrip("/") + "/", redirect_endpoint.lstrip("/"))

    # Validate domain
    callback_domain = _extract_domain(callback_url)
    main_domain = _extract_domain(main_url)

    if callback_domain != main_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain {callback_domain!r} is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    # Append the state parameter safely
    query = urllib.parse.urlencode({"state": session_state})
    parsed = urllib.parse.urlparse(callback_url)
    final_query = query if not parsed.query else f"{parsed.query}&{query}"
    final_url = urllib.parse.urlunparse(
        parsed._replace(query=final_query)
    )

    return final_url