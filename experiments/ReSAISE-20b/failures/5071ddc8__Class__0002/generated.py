#!/usr/bin/env python3
"""
Utility to safely assemble a redirect URI after authentication.

The function ensures that the resulting URL is either within the same
application domain or explicitly allowed in ALLOWED_DOMAINS. This protects
against open‑redirect vulnerabilities (CWE-610).

Author: ChatGPT
"""

from urllib.parse import urlparse, urljoin


# Example list of external domains that are considered safe for redirects.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]


def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    main_base_url : str
        The base authentication URL of the application (e.g., "https://app.example.com/").
    next_route : str
        The user‑supplied path or full URL to redirect to after login.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is outside the allowed domain list.
    """
    # Normalize base URL to ensure it ends with a slash for proper urljoin behavior
    if not main_base_url.endswith("/"):
        base = main_base_url + "/"
    else:
        base = main_base_url

    # Resolve the user supplied route against the base
    resolved = urljoin(base, next_route)

    parsed_resolved = urlparse(resolved)
    if not parsed_resolved.scheme or not parsed_resolved.netloc:
        # The resolved URL is a relative path (e.g., "/dashboard")
        # This is safe because it inherits the base's scheme/netloc
        return resolved

    # For absolute URLs, enforce domain checks
    base_parsed = urlparse(base)
    allowed_netlocs = {base_parsed.netloc.lower()}

    # Add allowed external domains (case-insensitive)
    for domain in ALLOWED_DOMAINS:
        # Accept subdomains of the allowed domain
        if parsed_resolved.netloc.lower().endswith(domain.lower()):
            return resolved

    # If not in allowed list, raise error
    raise ValueError(
        f"Unsafe redirect URL detected: {resolved}. "
        f"Allowed domains: {sorted(allowed_netlocs | set(ALLOWED_DOMAINS))}"
    )


# --------------------------- #
# Example usage (for testing)
# --------------------------- #
if __name__ == "__main__":
    try:
        print(assemble_redirect_uri("https://app.example.com", "/profile"))
        print(assemble_redirect_uri("https://app.example.com", "https://example.com/landing"))
        print(assemble_redirect_uri("https://app.example.com", "http://malicious.com/"))
    except ValueError as e:
        print(f"Redirect rejected: {e}")