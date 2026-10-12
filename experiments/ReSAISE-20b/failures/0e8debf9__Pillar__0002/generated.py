#!/usr/bin/env python3
"""
Secure redirect URL generator.

This module contains a single function `generate_redirect_uri` that safely builds
a full redirect URL after authentication. It validates the user supplied
`post_login_param` against a whitelist of allowed domains and ensures that
the final URL stays within the application domain or an approved external
domain.

Author: ChatGPT
"""

from urllib.parse import urlparse, urljoin, urlunparse

# List of external domains that are permitted for redirection.
ALLOWED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed.
}


def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    auth_base_url : str
        The base authentication URL of the application (e.g., "https://app.example.com").
    post_login_param : str
        The URL path or full URL the user intends to navigate to after login.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe (outside the base domain and not in ALLOWED_DOMAINS).
    """
    # Parse the authentication base URL.
    base_parsed = urlparse(auth_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid auth_base_url: {auth_base_url}")

    # Normalise the post_login_param.
    login_parsed = urlparse(post_login_param)

    # Case 1: Absolute URL (has scheme). Validate domain.
    if login_parsed.scheme in ("http", "https"):
        # If the hostname is exactly the same as the base, allow.
        if login_parsed.netloc == base_parsed.netloc:
            return post_login_param

        # If the hostname is in the allowed list, allow.
        if login_parsed.netloc.split(":")[0] in ALLOWED_DOMAINS:
            return post_login_param

        # Otherwise reject.
        raise ValueError(f"Disallowed redirect domain: {login_parsed.netloc}")

    # Case 2: Protocol-relative URL (e.g., "//evil.com").
    if login_parsed.scheme == "" and login_parsed.netloc:
        raise ValueError(f"Protocol-relative URLs are not allowed: {post_login_param}")

    # Case 3: Relative path or query (no scheme and no netloc).
    if not login_parsed.netloc:
        # Ensure it doesn't attempt to traverse outside the base path.
        # urljoin handles relative paths correctly, but we double‑check.
        joined = urljoin(auth_base_url.rstrip("/") + "/", login_parsed.path)
        # Append query and fragment if present.
        if login_parsed.query:
            joined = f"{joined}?{login_parsed.query}"
        if login_parsed.fragment:
            joined = f"{joined}#{login_parsed.fragment}"
        return joined

    # Any other case is considered unsafe.
    raise ValueError(f"Unsupported redirect format: {post_login_param}")


# Example usage (for testing purposes only; remove or guard under __main__ in production)
if __name__ == "__main__":
    try:
        print(generate_redirect_uri(
            "https://app.example.com",
            "/dashboard?view=summary"
        ))
        print(generate_redirect_uri(
            "https://app.example.com",
            "https://trustedpartner.org/welcome"
        ))
        # The following should raise ValueError
        print(generate_redirect_uri(
            "https://app.example.com",
            "http://malicious.com/steal"
        ))
    except ValueError as e:
        print(f"Error: {e}")