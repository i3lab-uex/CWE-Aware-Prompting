#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OAuth redirect URL builder with domain validation.

The module defines a single function, ``build_oauth_redirect_url``, which
constructs a secure callback URL for OAuth flows.  The function ensures that
the resulting URL points to an allowed domain or the same domain as the main
application.  This protects against CWE‑610 (Externally Controlled Reference to a Resource in Another Sphere).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Set


# --------------------------------------------------------------------------- #
# Allowed domains for OAuth callbacks.
#
# In a real application this set should be populated with the domains that
# are explicitly trusted to receive OAuth callbacks.  The empty set below
# means only the same‑domain callback is permitted.
# --------------------------------------------------------------------------- #
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    # "example.com",
    # "api.example.org",
}


def _extract_hostname(url: str) -> str:
    """
    Return the hostname of a URL, or raise ValueError if it cannot be parsed.
    """
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError(f"Unable to parse hostname from URL: {url!r}")
    return hostname.lower()


def build_oauth_redirect_url(
    main_url: str,
    redirect_endpoint: str,
    session_state: str,
) -> str:
    """
    Construct a secure OAuth callback URL.

    Parameters
    ----------
    main_url : str
        The root URL of the application (e.g. ``https://app.example.com``).
    redirect_endpoint : str
        The relative or absolute path that handles the OAuth callback.
        Examples: ``/auth/callback`` or ``https://app.example.com/auth/callback``.
    session_state : str
        A unique string (e.g. a UUID) that will be sent as the ``state``
        query parameter to mitigate CSRF attacks.

    Returns
    -------
    str
        The fully assembled OAuth callback URL, including the ``state`` query
        parameter.

    Raises
    ------
    ValueError
        If the resulting callback URL resolves to a domain that is not in
        ``ALLOWED_CALLBACK_DOMAINS`` and does not match the main application
        domain.
    """
    # 1. Resolve the full callback URL (relative to main_url if needed)
    resolved = urllib.parse.urljoin(main_url.rstrip("/") + "/", redirect_endpoint.lstrip("/"))
    callback_hostname = _extract_hostname(resolved)

    # 2. Resolve the main application hostname
    app_hostname = _extract_hostname(main_url)

    # 3. Domain validation
    if callback_hostname != app_hostname and callback_hostname not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback URL domain '{callback_hostname}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)!r} or same as main URL '{app_hostname}'."
        )

    # 4. Append the state parameter
    parsed = urllib.parse.urlparse(resolved)
    query_params = dict(urllib.parse.parse_qsl(parsed.query))
    query_params["state"] = session_state
    new_query = urllib.parse.urlencode(query_params)

    # 5. Reconstruct the final URL
    final_url = urllib.parse.urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment,
        )
    )

    return final_url


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test):
#
# if __name__ == "__main__":
#     main = "https://app.example.com"
#     endpoint = "/auth/callback"
#     state = "123e4567-e89b-12d3-a456-426614174000"
#     print(build_oauth_redirect_url(main, endpoint, state))
#
# --------------------------------------------------------------------------- #