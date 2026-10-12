#!/usr/bin/env python3
"""
Secure redirect URL generator.

This module defines a single function, `create_redirect_url`, which safely
constructs a redirect URL after successful authentication.  The function
ensures that the target is either within the same domain as the application
or belongs to a list of explicitly allowed external domains.  Any attempt to
redirect to an arbitrary host results in a ValueError.

The implementation follows best practices for preventing open‑redirect
vulnerabilities (CWE-601) and ensures that resources are properly validated
throughout their lifecycle.
"""

from urllib.parse import urlparse, urljoin

# Domains that are considered safe for redirection.  Add your own allowed
# domains here.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def _is_safe_domain(target_netloc: str, base_netloc: str) -> bool:
    """
    Determine if the target host is acceptable.

    Parameters
    ----------
    target_netloc : str
        The netloc (host[:port]) of the target URL.
    base_netloc : str
        The netloc (host[:port]) of the application's base URL.

    Returns
    -------
    bool
        True if the target host is either the same as the base or listed in
        ALLOWED_DOMAINS; False otherwise.
    """
    # Normalize: strip port for comparison
    target_host = target_netloc.split(":")[0].lower()
    base_host = base_netloc.split(":")[0].lower()

    if target_host == base_host:
        return True

    # Allow any port on the same host
    if target_netloc.lower() == base_netloc.lower():
        return True

    # Check against the allowed list
    for domain in ALLOWED_DOMAINS:
        if target_host == domain.lower():
            return True

    return False


def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    base_url : str
        The absolute base URL of the application (e.g., "https://app.example.com/").
    next_param : str
        The user-provided redirect target.  May be relative or absolute.

    Returns
    -------
    str
        A fully-qualified URL that is safe to redirect the user to.

    Raises
    ------
    ValueError
        If `next_param` resolves to a host that is not the same as
        `base_url` or an explicitly allowed external domain.
    """
    if not base_url:
        raise ValueError("Base URL must be provided.")

    # Parse the base URL to extract its components
    parsed_base = urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Base URL must be a fully-qualified absolute URL.")

    # Resolve the next_param against the base URL
    resolved_url = urljoin(base_url, next_param or "")

    parsed_resolved = urlparse(resolved_url)

    # If the resolved URL has a scheme (i.e., it's absolute), ensure its host
    # is allowed.  If it lacks a scheme, treat it as relative and prepend the
    # base URL's components.
    if parsed_resolved.scheme:
        if not _is_safe_domain(parsed_resolved.netloc, parsed_base.netloc):
            raise ValueError(
                f"Redirect target '{parsed_resolved.netloc}' is not allowed."
            )
    else:
        # Relative URLs are always safe; re-construct a full URL using the base
        resolved_url = urljoin(base_url, parsed_resolved.path)

    return resolved_url


# Example usage (uncomment for testing):
# if __name__ == "__main__":
#     print(create_redirect_url("https://app.example.com/", "/dashboard"))
#     print(create_redirect_url("https://app.example.com/", "https://trustedpartner.org/home"))
#     # The following would raise ValueError:
#     # print(create_redirect_url("https://app.example.com/", "http://malicious.com/"))