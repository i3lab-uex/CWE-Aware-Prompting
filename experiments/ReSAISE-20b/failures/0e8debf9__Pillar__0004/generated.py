#!/usr/bin/env python3
"""
Utility to generate a safe redirect URI after authentication.

The function ensures that the resulting URL is either within the same
application domain or belongs to a pre‑approved external domain list.
"""

from urllib.parse import urlparse, urljoin
from typing import List

# Pre‑approved external domains for redirects (example)
ALLOWED_DOMAINS: List[str] = [
    "trusted.com",
    "partner.org",
    # Add more domains as needed
]


def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Construct a safe redirect URL by appending the user supplied `post_login_param`
    to the base authentication URL.

    Parameters
    ----------
    auth_base_url : str
        Base URL of the application (e.g. "https://app.example.com/").
    post_login_param : str
        URL path or full URL the user wishes to navigate to after login.

    Returns
    -------
    str
        The resolved, fully‑qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unsafe location:
            * Not within the same domain as `auth_base_url`, and
            * Not listed in :data:`ALLOWED_DOMAINS`.
    """
    # Resolve the final URL
    resolved_url = urljoin(auth_base_url, post_login_param)

    # Parse components for validation
    parsed_resolved = urlparse(resolved_url)
    parsed_base = urlparse(auth_base_url)

    # Helper to extract the domain part (netloc without port)
    def _domain(netloc: str) -> str:
        return netloc.split(":")[0].lower()

    resolved_domain = _domain(parsed_resolved.netloc)
    base_domain = _domain(parsed_base.netloc)

    # If the resolved domain is exactly the same as the base, it's safe
    if resolved_domain == base_domain:
        return resolved_url

    # Otherwise, check against the allowed external domains list
    if resolved_domain in (d.lower() for d in ALLOWED_DOMAINS):
        return resolved_url

    # If none of the checks pass, reject the URL
    raise ValueError(
        f"Unsafe redirect detected: '{resolved_url}' "
        f"does not belong to the base domain or allowed domains."
    )


# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     base = "https://app.example.com/"
#     print(generate_redirect_uri(base, "/dashboard"))
#     print(generate_redirect_uri(base, "https://trusted.com/welcome"))
#     # The following would raise ValueError
#     # print(generate_redirect_uri(base, "https://evil.com/phish"))