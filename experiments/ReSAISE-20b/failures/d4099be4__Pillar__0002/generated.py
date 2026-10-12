#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility to generate a secure OAuth callback URL.

The function validates that the constructed callback URL resolves
to one of the domains listed in ``ALLOWED_CALLBACK_DOMAINS``.
"""

from urllib.parse import urljoin, urlencode, urlparse
from typing import Iterable

# --------------------------------------------------------------------------- #
# Allowed callback domains – replace or extend as needed.
ALLOWED_CALLBACK_DOMAINS: Iterable[str] = {
    "example.com",
    "app.example.org",
}

# --------------------------------------------------------------------------- #
def generate_oauth_callback_link(
    app_base_url: str,
    callback_endpoint: str,
    verification_state: str
) -> str:
    """
    Construct a fully-qualified OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The application's base URL (e.g., "https://app.example.org").
    callback_endpoint : str
        The relative path for the OAuth callback (e.g., "/auth/callback").
    verification_state : str
        A unique value used to verify the integrity of the OAuth flow.

    Returns
    -------
    str
        The final callback URL, e.g.:
        "https://app.example.org/auth/callback?state=xyz".

    Raises
    ------
    ValueError
        If the resulting URL's domain is not in ``ALLOWED_CALLBACK_DOMAINS``.
    """
    # Ensure the base URL ends with a slash to avoid mis‑joining
    if not app_base_url.endswith("/"):
        base = f"{app_base_url}/"
    else:
        base = app_base_url

    # Join the base URL with the callback endpoint
    joined_url = urljoin(base, callback_endpoint.lstrip("/"))

    # Append the state query parameter
    parsed = urlparse(joined_url)
    query_params = dict()
    if parsed.query:
        # Preserve any existing query parameters
        for key, value in [p.split("=") for p in parsed.query.split("&") if "=" in p]:
            query_params[key] = value
    query_params["state"] = verification_state

    final_query = urlencode(query_params)
    callback_url = (
        f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        + (f"?{final_query}" if final_query else "")
    )

    # Validate domain against allowed list
    hostname = parsed.hostname or ""
    if hostname.lower() not in {d.lower() for d in ALLOWED_CALLBACK_DOMAINS}:
        raise ValueError(
            f"Callback URL domain '{hostname}' is not allowed. "
            f"Allowed domains: {sorted(ALLOWED_CALLBACK_DOMAINS)}"
        )

    return callback_url

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage
    try:
        url = generate_oauth_callback_link(
            "https://app.example.org",
            "/oauth/callback",
            "unique_state_value_123"
        )
        print("Generated callback URL:", url)
    except ValueError as e:
        print(f"Error: {e}")