#!/usr/bin/env python3
"""
Utility for building a Single Sign-On (SSO) redirect URL.

The `construct_sso_redirect` function validates the provided return
URL against a whitelist of allowed domains and then assembles the full
SSO redirect URL with the necessary query parameters.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Set


# --------------------------------------------------------------------------- #
# Configuration: list of domains that are allowed as return URLs.
# In a real application this would be loaded from configuration or environment
# variables rather than hard‑coded.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
    # Add additional domains as needed
}
# --------------------------------------------------------------------------- #


def _extract_domain(netloc: str) -> str:
    """
    Extract the hostname from a netloc string, stripping any port.
    """
    return urllib.parse.splitport(netloc)[0].lower()


def construct_sso_redirect(
    auth_service_endpoint: str,
    user_identifier: str,
    redirect_uri: str,
) -> str:
    """
    Build a complete SSO redirect URL.

    Parameters
    ----------
    auth_service_endpoint : str
        The base URL of the SSO provider.
    user_identifier : str
        Unique identifier for the user (e.g. a user ID or username).
    redirect_uri : str
        The URL to which the provider should redirect after authentication.

    Returns
    -------
    str
        A fully formed URL that can be used to redirect the user for SSO.

    Raises
    ------
    ValueError
        If the domain of ``redirect_uri`` is not in :data:`ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect_uri domain
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    if not parsed_redirect.scheme or not parsed_redirect.netloc:
        raise ValueError(f"Invalid redirect_uri: {redirect_uri!r}")

    domain = _extract_domain(parsed_redirect.netloc)
    if domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Redirect URI domain '{domain}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_RETURN_DOMAINS)}"
        )

    # Build the query parameters
    query_params = {
        "user": user_identifier,
        "redirect_uri": redirect_uri,  # The provider may expect this to be URL‑encoded
    }

    # Parse the auth service endpoint and merge query parameters
    parsed_endpoint = urllib.parse.urlparse(auth_service_endpoint)
    # Preserve existing query params if any
    existing_params = urllib.parse.parse_qs(parsed_endpoint.query, keep_blank_values=True)
    # Merge with new params (new values overwrite existing keys)
    merged_params = {k: v[0] for k, v in existing_params.items()}
    merged_params.update(query_params)

    # Reconstruct the full URL
    new_query = urllib.parse.urlencode(merged_params, doseq=False)
    redirect_url = urllib.parse.ParseResult(
        scheme=parsed_endpoint.scheme,
        netloc=parsed_endpoint.netloc,
        path=parsed_endpoint.path or "/",
        params=parsed_endpoint.params,
        query=new_query,
        fragment=parsed_endpoint.fragment,
    ).geturl()

    return redirect_url


# --------------------------------------------------------------------------- #
# Example usage (would normally be in a separate test module or main block)
if __name__ == "__main__":
    try:
        url = construct_sso_redirect(
            auth_service_endpoint="https://sso.example.com/auth",
            user_identifier="alice123",
            redirect_uri="https://app.example.com/dashboard?foo=bar",
        )
        print(f"Redirect URL: {url}")
    except ValueError as exc:
        print(f"Error constructing redirect URL: {exc}")