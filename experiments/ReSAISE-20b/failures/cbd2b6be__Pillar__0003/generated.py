#!/usr/bin/env python3
"""
Utility for constructing a secure OAuth callback URL.

The function validates that the resulting redirect URL's domain is
whitelisted, then appends a state query parameter to protect against CSRF.
"""

from __future__ import annotations

import urllib.parse
from typing import Iterable


# Example whitelist – replace with your own allowed domains.
ALLOWED_CALLBACK_DOMAINS: set[str] = {"example.com", "auth.myapp.org"}


def build_oauth_redirect_url(
    main_url: str,
    redirect_path: str,
    token_state: str,
) -> str:
    """
    Construct a fully‑qualified OAuth redirect URL.

    Parameters
    ----------
    main_url : str
        The base URL of the application (e.g., "https://myapp.com").
    redirect_path : str
        The path to the OAuth callback endpoint (e.g., "/auth/callback").
    token_state : str
        A unique, unpredictable value used to validate the OAuth flow.

    Returns
    -------
    str
        The validated redirect URL with a `state` query parameter.

    Raises
    ------
    ValueError
        If the final URL's domain is not in :data:`ALLOWED_CALLBACK_DOMAINS`
        or if the ``token_state`` is empty.
    """
    # Basic sanity checks
    if not token_state:
        raise ValueError("token_state must be a non‑empty string")

    # Parse the main URL
    parsed_main = urllib.parse.urlparse(main_url)
    if not parsed_main.scheme or not parsed_main.netloc:
        raise ValueError(f"Invalid main_url: {main_url!r}")

    # Resolve the redirect path against the base
    resolved_path = urllib.parse.urljoin(parsed_main.path + "/", redirect_path.lstrip("/"))

    # Build the new URL components
    new_parts = list(parsed_main)
    new_parts[2] = resolved_path  # path
    # Append the state query parameter safely
    qs_dict = urllib.parse.parse_qs(parsed_main.query)
    qs_dict["state"] = [token_state]
    new_parts[4] = urllib.parse.urlencode(qs_dict, doseq=True)

    final_url = urllib.parse.urlunparse(new_parts)

    # Verify the domain is allowed
    final_netloc = urllib.parse.urlparse(final_url).netloc
    # Strip port if present for comparison
    domain = final_netloc.split(":")[0]
    if domain not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Redirect domain {domain!r} is not in the list of allowed domains"
        )

    return final_url


# Example usage
if __name__ == "__main__":
    try:
        url = build_oauth_redirect_url(
            main_url="https://myapp.com",
            redirect_path="/oauth/callback",
            token_state="1234567890abcdef",
        )
        print("OAuth Redirect URL:", url)
    except ValueError as exc:
        print(f"Error constructing redirect URL: {exc}")