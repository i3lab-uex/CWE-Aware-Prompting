#!/usr/bin/env python3
"""
Utility to create a safe redirect URL after login.
"""

from urllib.parse import urlparse, urljoin
from typing import List

# Example list of external domains that are considered safe for redirection.
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedsite.org",
    # Add other domains as needed
]


def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Construct a safe redirect URL based on the application home URL and
    a user-provided forward parameter.

    Parameters
    ----------
    app_home_url : str
        Base URL of the application (e.g. "https://myapp.example.com/").
    forward_param : str
        Desired path or URL the user wants to be redirected to after login.
        May be a relative path (e.g. "/dashboard") or an absolute URL
        pointing to an allowed external domain.

    Returns
    -------
    str
        The fully qualified redirect URL that is safe to use in a redirect.

    Raises
    ------
    ValueError
        If the forward_param leads to an unsafe URL:
          * contains a scheme (e.g. "http://") that is not allowed,
          * resolves to a domain that is neither the app's domain nor in
            ALLOWED_DOMAINS,
          * or otherwise cannot be safely constructed.
    """
    # Parse the base URL to extract its components
    parsed_base = urlparse(app_home_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("app_home_url must be a fully qualified URL with scheme and domain")

    # Reject forward_param that contains a scheme (e.g. "http://...")
    parsed_forward = urlparse(forward_param)
    if parsed_forward.scheme:
        # If the scheme is present, ensure it points to an allowed domain
        if parsed_forward.netloc not in ALLOWED_DOMAINS:
            raise ValueError(f"Redirection to external domain '{parsed_forward.netloc}' is not allowed")
        # It's an absolute URL but already safe; return it unchanged
        final_url = forward_param
    else:
        # It's a relative path; join with the base URL
        final_url = urljoin(app_home_url, forward_param)

    # Verify that the resulting URL's domain is safe
    parsed_final = urlparse(final_url)
    if not parsed_final.scheme or not parsed_final.netloc:
        # Should never happen because urljoin/urlparse guarantees scheme/netloc
        raise ValueError("Constructed URL is missing scheme or domain")

    # Allow the app's own domain
    if parsed_final.netloc == parsed_base.netloc:
        return final_url

    # Allow any domain listed in ALLOWED_DOMAINS
    if parsed_final.netloc in ALLOWED_DOMAINS:
        return final_url

    raise ValueError(f"Redirect URL domain '{parsed_final.netloc}' is not allowed")

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(create_forward_link("https://myapp.example.com/", "/dashboard"))
#     print(create_forward_link("https://myapp.example.com/", "https://trustedsite.org/welcome"))
#     # This will raise ValueError
#     # print(create_forward_link("https://myapp.example.com/", "http://malicious.com/"))