#!/usr/bin/env python3
"""
Secure redirect URL generator.

The function `generate_redirect_uri` constructs a full URL for redirecting
after authentication.  It validates the supplied target against a whitelist
of allowed domains and ensures that redirects cannot lead to arbitrary
external sites (CWE‑601).

Author: OpenAI ChatGPT
"""

from urllib.parse import urlparse, urljoin
from typing import List

# Pre‑approved external domains that may be used in redirects.
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
    "another-allowed-site.net",
]

def _is_allowed_domain(netloc: str) -> bool:
    """
    Check whether the given network location is in the allowed domains list.
    The comparison is case‑insensitive and ignores port numbers.

    Parameters
    ----------
    netloc : str
        The network location part of a URL (host[:port]).

    Returns
    -------
    bool
        True if the domain is allowed, False otherwise.
    """
    host = netloc.split(":")[0].lower()
    return any(host == allowed.lower() for allowed in ALLOWED_DOMAINS)


def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Generate a safe redirect URL after login.

    The function joins the base authentication URL with the user‑supplied
    target path or full URL, then validates that the resulting redirect
    remains within the same domain as `auth_base_url` or is explicitly
    whitelisted in ``ALLOWED_DOMAINS``.  Any attempt to redirect to an
    unapproved external domain raises ``ValueError``.

    Parameters
    ----------
    auth_base_url : str
        Base URL of the authentication application (e.g. ``https://app.example.com``).
    post_login_param : str
        Path or full URL to redirect to after login.

    Returns
    -------
    str
        The fully resolved and validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe (redirects to an unapproved domain).
    """
    if not auth_base_url:
        raise ValueError("auth_base_url must be provided")

    # Parse the base URL to obtain its scheme and netloc
    base_parsed = urlparse(auth_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("auth_base_url must be a valid absolute URL")

    # Construct the candidate redirect URL
    candidate = urljoin(auth_base_url, post_login_param)

    # Parse the candidate to inspect its components
    parsed_candidate = urlparse(candidate)

    # If the candidate has a scheme, it is an absolute URL.
    if parsed_candidate.scheme:
        # Allow only http/https schemes
        if parsed_candidate.scheme not in {"http", "https"}:
            raise ValueError(f"Unsupported URL scheme: {parsed_candidate.scheme}")

        # If the host matches the base, it's safe
        if parsed_candidate.netloc.lower() == base_parsed.netloc.lower():
            return candidate

        # Otherwise, the host must be in the allowed domains list
        if _is_allowed_domain(parsed_candidate.netloc):
            return candidate

        # Not allowed: raise error
        raise ValueError(f"Redirect to unapproved domain: {parsed_candidate.netloc}")

    # If the candidate is relative, it will be resolved to the same host as base
    # but we still need to ensure that no leading '//' (scheme‑relative) sneaks in
    if parsed_candidate.scheme == "" and parsed_candidate.netloc != "":
        # e.g., "//evil.com/path" is scheme‑relative and bypasses the check above
        raise ValueError("Scheme-relative URLs are not allowed")

    # At this point, the candidate is a relative path within the same domain
    return candidate

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     print(generate_redirect_uri("https://app.example.com/login", "/dashboard"))
#     print(generate_redirect_uri("https://app.example.com/login", "https://trustedpartner.org/welcome"))
#     # The following would raise ValueError
#     # print(generate_redirect_uri("https://app.example.com/login", "http://malicious.com/"))