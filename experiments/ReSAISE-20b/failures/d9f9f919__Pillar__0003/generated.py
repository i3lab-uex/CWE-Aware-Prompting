#!/usr/bin/env python3
"""
Utility to construct a safe redirect URL after authentication.
"""

from urllib.parse import urlparse, urlunparse
from typing import List

# Example list of domains that are allowed to be redirected to externally.
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trusted.org",
    # Add more domains as needed.
]


def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a full redirect URL by combining the application's base URL with
    the user supplied `redirect_param`.

    Parameters
    ----------
    app_base_url : str
        Base URL of the application (e.g., "https://app.example.com").
    redirect_param : str
        Path or full URL to which the user wants to be redirected after login.
        May be a relative path (e.g., "/dashboard") or an absolute URL.

    Returns
    -------
    str
        A fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe: it points to a domain that is neither
        the application's own nor one of the allowed external domains.
    """
    # Parse base URL and redirect param
    base = urlparse(app_base_url.rstrip("/"))
    if not base.scheme or not base.netloc:
        raise ValueError(f"Invalid application base URL: {app_base_url!r}")

    # Resolve the redirect target
    redirect = urlparse(redirect_param)

    if redirect.scheme and redirect.netloc:
        # Absolute URL provided by the user
        target_netloc = redirect.netloc.lower()
        base_domain = base.netloc.lower()

        # If the target domain matches the application, keep it as is.
        if target_netloc == base_domain:
            resolved = redirect
        else:
            # Check against the whitelist of allowed external domains.
            if target_netloc not in {d.lower() for d in ALLOWED_DOMAINS}:
                raise ValueError(f"Redirect to external domain {target_netloc!r} is not allowed")
            resolved = redirect
    else:
        # Relative path; combine with base URL.
        # Ensure the path starts with '/' to avoid malformed URLs.
        relative_path = redirect.path
        if not relative_path.startswith("/"):
            relative_path = "/" + relative_path

        # Preserve any query or fragment from the redirect_param.
        resolved = base._replace(path=relative_path, query=redirect.query,
                                 fragment=redirect.fragment)

    # Construct the final URL string
    final_url = urlunparse(resolved)
    return final_url


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    try:
        print(build_redirect_link("https://app.example.com", "/profile"))
        print(build_redirect_link("https://app.example.com",
                                  "https://trusted.org/welcome?ref=login"))
        # This will raise ValueError
        print(build_redirect_link("https://app.example.com",
                                  "https://malicious.site/phish"))
    except ValueError as exc:
        print(f"Redirect error: {exc}")