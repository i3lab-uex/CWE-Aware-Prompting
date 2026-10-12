#!/usr/bin/env python3
"""
SSO redirect URL constructor.

The function `construct_sso_redirect` builds a secure SSO redirect URL by
validating the destination domain, encoding parameters, and appending them
to the SSO endpoint.  It follows best practices to mitigate common web
security issues (e.g., open redirect attacks, injection).

CWE-664 is addressed by ensuring that the SSO endpoint and the return URL
are fully controlled before any external resources are accessed.
"""

from __future__ import annotations

import urllib.parse
from typing import Set


# Example whitelist – replace with your actual allowed domains.
ALLOWED_RETURN_DOMAINS: Set[str] = {
    "example.com",
    "myapp.example.org",
}


def _extract_domain(url: str) -> str:
    """
    Extract the domain (netloc) from a URL, stripping any port.
    Raises ValueError if the URL is malformed or missing netloc.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Malformed URL: {url!r}")
    # Remove port if present
    return parsed.hostname.lower() if parsed.hostname else ""


def construct_sso_redirect(
    sso_uri: str,
    user_identifier: str,
    redirect_link: str,
) -> str:
    """
    Construct an SSO redirect URL.

    Parameters
    ----------
    sso_uri : str
        Base SSO endpoint (e.g., "https://auth.example.com/sso").
    user_identifier : str
        Unique identifier for the user (e.g., a UUID or email).
    redirect_link : str
        Destination URL after SSO completion.

    Returns
    -------
    str
        Full SSO redirect URL with encoded parameters.

    Raises
    ------
    ValueError
        If the domain of `redirect_link` is not in `ALLOWED_RETURN_DOMAINS`.
    """
    # Validate the redirect link domain
    dest_domain = _extract_domain(redirect_link)
    if dest_domain not in ALLOWED_RETURN_DOMAINS:
        raise ValueError(
            f"Redirect domain {dest_domain!r} is not allowed. "
            "Allowed domains: " + ", ".join(sorted(ALLOWED_RETURN_DOMAINS))
        )

    # Parse the base SSO URI to ensure it is valid
    parsed_sso = urllib.parse.urlparse(sso_uri)
    if not parsed_sso.scheme or not parsed_sso.netloc:
        raise ValueError(f"Malformed SSO URI: {sso_uri!r}")

    # Build query parameters safely
    query_params = {
        "user_id": user_identifier,
        "redirect_uri": redirect_link,
    }
    encoded_query = urllib.parse.urlencode(query_params, doseq=True)

    # Construct the final URL
    sso_url = urllib.parse.urlunparse(
        (
            parsed_sso.scheme,
            parsed_sso.netloc,
            parsed_sso.path,
            parsed_sso.params,
            encoded_query,
            parsed_sso.fragment,
        )
    )

    return sso_url


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         url = construct_sso_redirect(
#             sso_uri="https://auth.example.com/sso",
#             user_identifier="user-12345",
#             redirect_link="https://myapp.example.org/dashboard"
#         )
#         print(url)
#     except ValueError as exc:
#         print(f"Error: {exc}")