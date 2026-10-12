#!/usr/bin/env python3
"""
Utility to generate a secure OAuth callback URL.

The function ensures that the final URL points to one of the
pre‑approved domains, protecting against CWE-610 (Externally Controlled
Reference to a Resource in Another Sphere).
"""

from urllib.parse import urlparse, urljoin, urlencode
from typing import Iterable

# Pre‑defined set of allowed callback domains.
ALLOWED_CALLBACK_DOMAINS: frozenset[str] = frozenset(
    {
        "example.com",
        "auth.example.org",
        "oauth.callback.local",
    }
)


def generate_oauth_callback_link(
    app_base_url: str,
    callback_endpoint: str,
    verification_state: str,
) -> str:
    """
    Construct a fully‑qualified OAuth callback URL.

    Parameters
    ----------
    app_base_url : str
        The application's base URL (e.g., "https://app.example.com").
    callback_endpoint : str
        The path for the OAuth callback endpoint (e.g., "/auth/callback").
    verification_state : str
        A unique value to be passed as the `state` query parameter.

    Returns
    -------
    str
        The complete OAuth callback URL with the `state` query parameter.

    Raises
    ------
    ValueError
        If the domain of the constructed URL is not in :data:`ALLOWED_CALLBACK_DOMAINS`.
    """
    # Ensure the base URL ends with a slash for proper urljoin behavior
    if not app_base_url.endswith("/"):
        base = f"{app_base_url}/"
    else:
        base = app_base_url

    # Normalize the callback endpoint: strip leading slashes to avoid
    # overriding the base path when joined.
    endpoint = callback_endpoint.lstrip("/")

    # Build the URL and append the state parameter
    url_without_query = urljoin(base, endpoint)
    query_string = urlencode({"state": verification_state})
    full_url = f"{url_without_query}?{query_string}"

    # Validate the domain
    parsed = urlparse(full_url)
    domain = parsed.hostname

    if not domain or domain.lower() not in ALLOWED_CALLBACK_DOMAINS:
        raise ValueError(
            f"Disallowed callback domain '{domain}'. "
            f"Allowed domains: {', '.join(sorted(ALLOWED_CALLBACK_DOMAINS))}"
        )

    return full_url


# Example usage (for demonstration only; remove or comment out in production)
if __name__ == "__main__":
    try:
        link = generate_oauth_callback_link(
            app_base_url="https://app.example.com",
            callback_endpoint="/oauth/callback",
            verification_state="abc123xyz",
        )
        print("Generated callback URL:", link)
    except ValueError as exc:
        print(f"Error: {exc}")