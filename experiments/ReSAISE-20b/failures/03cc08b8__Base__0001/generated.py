#!/usr/bin/env python3
"""
Utility to assemble a secure OAuth callback URL.

The function verifies that the resulting URL stays within an allowed set of
domains or the same domain as the application. It also protects against open
redirect attacks by rejecting absolute URLs in the callback route.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import urllib.parse
from typing import Set

# Example set of allowed callback domains.
# In a real application, this should be populated from configuration or environment.
ALLOWED_CALLBACK_DOMAINS: Set[str] = {
    "example.com",
    "auth.example.org",
}

def assemble_oauth_callback(
    application_url: str,
    callback_route: str,
    token_state: str,
) -> str:
    """
    Construct a fully qualified OAuth callback URL.

    Parameters
    ----------
    application_url : str
        The base URL of the application (e.g. "https://app.example.com").
    callback_route : str
        The path or relative URL where the OAuth provider should redirect.
        Must be a relative path (no scheme or netloc).
    token_state : str
        A unique identifier that will be appended as the `state` query parameter.

    Returns
    -------
    str
        The fully assembled OAuth callback URL, including the `state` parameter.

    Raises
    ------
    ValueError
        If the callback route is absolute or if the resulting URL's domain is not
        in :data:`ALLOWED_CALLBACK_DOMAINS` or the application's own domain.
    """
    # 1. Validate callback_route is a relative path
    parsed_callback = urllib.parse.urlparse(callback_route)
    if parsed_callback.scheme or parsed_callback.netloc:
        raise ValueError(
            f"callback_route must be a relative path, got absolute URL: {callback_route}"
        )

    # 2. Parse the application base URL
    parsed_app = urllib.parse.urlparse(application_url)
    if not parsed_app.scheme or not parsed_app.netloc:
        raise ValueError(f"Invalid application_url: {application_url}")

    # 3. Build the absolute callback URL
    # urljoin will correctly handle leading slashes in callback_route
    base_url = urllib.parse.urlunparse(
        (parsed_app.scheme, parsed_app.netloc, "", "", "", "")
    )
    absolute_callback = urllib.parse.urljoin(base_url, callback_route)

    # 4. Append the state query parameter
    parsed_abs = urllib.parse.urlparse(absolute_callback)
    # Preserve existing query parameters, if any
    qs = dict(urllib.parse.parse_qsl(parsed_abs.query))
    qs["state"] = token_state
    new_query = urllib.parse.urlencode(qs)

    final_url = urllib.parse.urlunparse(
        (
            parsed_abs.scheme,
            parsed_abs.netloc,
            parsed_abs.path,
            parsed_abs.params,
            new_query,
            parsed_abs.fragment,
        )
    )

    # 5. Security check: ensure domain is allowed
    final_domain = parsed_abs.netloc.split(":")[0].lower()
    app_domain = parsed_app.netloc.split(":")[0].lower()

    if final_domain not in ALLOWED_CALLBACK_DOMAINS and final_domain != app_domain:
        raise ValueError(
            f"Disallowed callback domain: {final_domain}. "
            f"Allowed domains are: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    return final_url

# Example usage (uncomment to test)
if __name__ == "__main__":
    try:
        url = assemble_oauth_callback(
            "https://app.example.com",
            "/oauth/callback",
            "abc123state"
        )
        print(url)
    except ValueError as exc:
        print(f"Error assembling OAuth callback URL: {exc}")