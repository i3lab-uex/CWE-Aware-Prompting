#!/usr/bin/env python3
"""
Utility for generating a safe redirect URL after login.

The function ensures that the target URL is either relative to the
application or points to an explicitly approved external domain.
"""

from urllib.parse import urlparse, urljoin
from typing import List


# Domains that are allowed to be redirected to (e.g. external partner sites)
APPROVED_DOMAINS: List[str] = [
    "example.com",
    "partner.example.org",
]


def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    app_url : str
        The base URL of the application (e.g. "https://myapp.com/").
    redirect_param : str
        The URL path or full URL supplied by the user to navigate to after login.

    Returns
    -------
    str
        A fully resolved redirect URL that is guaranteed to stay within the
        application domain or one of the approved external domains.

    Raises
    ------
    ValueError
        If the resolved URL resolves to a domain that is neither the same as
        `app_url` nor listed in :data:`APPROVED_DOMAINS`.
    """
    # Normalise the base URL
    parsed_app = urlparse(app_url)
    if not parsed_app.scheme or not parsed_app.netloc:
        raise ValueError(f"Invalid application URL: {app_url!r}")

    # Resolve the redirect target against the base URL
    resolved = urljoin(app_url, redirect_param)

    # Parse the resulting URL to inspect its components
    parsed_resolved = urlparse(resolved)

    # If the redirect is relative, it will inherit the base scheme/netloc
    if not parsed_resolved.scheme:
        # This shouldn't happen because urljoin always returns an absolute URL
        parsed_resolved = parsed_app._replace(path=parsed_resolved.path)

    # Check that the target domain is allowed
    target_domain = parsed_resolved.hostname or ""
    if target_domain == parsed_app.hostname:
        # Target is within the application domain – OK
        return resolved

    if target_domain in APPROVED_DOMAINS:
        # Target is an approved external domain – OK
        return resolved

    # Anything else is disallowed
    raise ValueError(
        f"Redirect target {target_domain!r} is not allowed. "
        "Must be within the application or an approved domain."
    )


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
#
# if __name__ == "__main__":
#     base = "https://myapp.com/"
#     for param in [
#         "/dashboard",
#         "../admin",          # should resolve to myapp.com/admin
#         "https://example.com/welcome",
#         "http://evil.com/steal",
#     ]:
#         try:
#             print(generate_redirect_link(base, param))
#         except ValueError as exc:
#             print(f"Rejecting {param!r}: {exc}")