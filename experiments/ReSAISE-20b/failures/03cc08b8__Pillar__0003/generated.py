#!/usr/bin/env python3
"""
Utility to assemble a secure OAuth callback URL.
"""

from __future__ import annotations

import urllib.parse
from typing import Set


# --------------------------------------------------------------------------- #
# Configuration – normally this would be imported from a config module.
# The set must contain only fully-qualified domain names (no schemes, no paths).
ALLOWED_CALLBACK_DOMAINS: Set[str] = {"example.com", "auth.example.org"}
# --------------------------------------------------------------------------- #


def assemble_oauth_callback(
    application_url: str,
    callback_route: str,
    token_state: str,
) -> str:
    """
    Build a fully-qualified OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The base URL of the application (e.g. "https://app.example.com").
    callback_route : str
        The route path for the OAuth callback handler (e.g. "/auth/callback").
    token_state : str
        A unique identifier that will be passed as the ``state`` query parameter.

    Returns
    -------
    str
        The fully assembled callback URL, e.g.
        "https://app.example.com/auth/callback?state=xyz".

    Raises
    ------
    ValueError
        If the resulting callback URL's domain is not in
        :data:`ALLOWED_CALLBACK_DOMAINS` and does not match the domain of
        ``application_url``.
    """
    # ----------------------------------------------------------------------- #
    # 1. Sanitize inputs and build the base callback URL
    # ----------------------------------------------------------------------- #

    # Ensure the application_url is a valid absolute URL.
    parsed_app = urllib.parse.urlparse(application_url)
    if not (parsed_app.scheme and parsed_app.netloc):
        raise ValueError(f"Invalid application_url: {application_url!r}")

    # Prevent callback_route from containing a scheme or netloc
    if urllib.parse.urlparse(callback_route).scheme:
        raise ValueError("callback_route must be a relative path, not an absolute URL")

    # Join the base URL with the callback route
    joined = urllib.parse.urljoin(application_url.rstrip("/") + "/", callback_route.lstrip("/"))
    parsed_joined = urllib.parse.urlparse(joined)

    # ----------------------------------------------------------------------- #
    # 2. Validate the domain of the callback URL
    # ----------------------------------------------------------------------- #

    callback_domain = parsed_joined.hostname  # may be None if malformed
    app_domain = parsed_app.hostname

    if callback_domain is None:
        raise ValueError(f"Resulting URL has no hostname: {joined!r}")

    # The domain must either be the same as the application or in the allowed set
    if callback_domain != app_domain and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Callback domain {callback_domain!r} is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    # ----------------------------------------------------------------------- #
    # 3. Append the state query parameter safely
    # ----------------------------------------------------------------------- #

    # Parse existing query parameters (if any)
    query_params = dict(urllib.parse.parse_qsl(parsed_joined.query, keep_blank_values=True))

    # Add or overwrite the state parameter
    query_params["state"] = token_state

    # Rebuild the query string, ensuring proper encoding
    encoded_query = urllib.parse.urlencode(query_params)

    # Reconstruct the full URL
    assembled_url = urllib.parse.urlunparse(
        (
            parsed_joined.scheme,
            parsed_joined.netloc,
            parsed_joined.path,
            parsed_joined.params,
            encoded_query,
            parsed_joined.fragment,
        )
    )

    return assembled_url