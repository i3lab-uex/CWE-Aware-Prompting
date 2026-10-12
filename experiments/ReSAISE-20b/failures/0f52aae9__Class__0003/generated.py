#!/usr/bin/env python3
"""
Utility to build a secure OAuth redirect URL.

The function validates that the resulting callback URL is either on one of
the explicitly allowed domains or, if no explicit domain list is supplied,
falls back to the same domain as ``main_url``.  This guards against
CWE‑610 – externally controlled reference to a resource in another sphere.
"""

from __future__ import annotations

import urllib.parse
from typing import Iterable, Set


# Example set of allowed callback domains.  In a real application this
# would probably be loaded from configuration or environment variables.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "auth.example.com",
    "oauth.callback.org",
}


def _extract_domain(url: str) -> str:
    """
    Return the network location part of a URL, lower‑cased.
    Raises ValueError if the URL is malformed or missing a netloc.
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
        The base URL of the application (e.g., ``https://app.example.com``).
    redirect_endpoint : str
        The endpoint that will handle the OAuth callback (e.g., ``/oauth/callback``).
    session_state : str
        A unique identifier used to protect against CSRF attacks.

    Returns
    -------
    str
        The fully assembled redirect URL with a ``state`` query parameter.

    Raises
    ------
    ValueError
        If the callback URL domain is not in ``ALLOWED_CALLBACK_DOMAINS`` and
        does not match the domain of ``main_url``.
    """
    # Build the absolute callback URL
    base = urllib.parse.urljoin(main_url.rstrip("/") + "/", redirect_endpoint.lstrip("/"))
    parsed_base = urllib.parse.urlparse(base)

    # Validate the domain
    callback_domain = _extract_domain(base)
    main_domain = _extract_domain(main_url)

    if ALLOWED_CALLBACK_DOMAINS and callback_domain not in ALLOWED_CALLBACK_DOMAINS:
        # If an explicit list is provided, it must contain the domain
        raise ValueError(
            f"Callback domain {callback_domain!r} is not in the allowed list."
        )

    if callback_domain != main_domain:
        # If no explicit list or domain not allowed, enforce same‑domain rule
        raise ValueError(
            f"Callback domain {callback_domain!r} does not match main application domain {main_domain!r}."
        )

    # Append the state parameter safely
    query = urllib.parse.parse_qs(parsed_base.query)
    query["state"] = [session_state]
    new_query = urllib.parse.urlencode(query, doseq=True)

    # Reconstruct the full URL
    final_url = urllib.parse.urlunparse(
        (
            parsed_base.scheme,
            parsed_base.netloc,
            parsed_base.path,
            parsed_base.params,
            new_query,
            parsed_base.fragment,
        )
    )

    return final_url


# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    try:
        url = build_oauth_redirect_url(
            main_url="https://app.example.com",
            redirect_endpoint="/oauth/callback",
            session_state="xyz123",
        )
        print("OAuth Redirect URL:", url)
    except ValueError as exc:
        print("URL validation error:", exc)