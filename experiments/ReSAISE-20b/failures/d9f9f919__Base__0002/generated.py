#!/usr/bin/env python3
"""
Safe redirect link builder to mitigate CWE-601 (Open Redirect).

The function validates the supplied redirect target against a list of
allowed domains and ensures that relative paths are resolved correctly.
"""

from urllib.parse import urlparse, urljoin
import re

# Example allowed external domains. In a real application this list should be
# loaded from configuration or environment variables.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

# Regular expression to match a valid domain name.
_DOMAIN_RE = re.compile(
    r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+"
    r"(?:[a-zA-Z]{2,63}))$",
    re.IGNORECASE,
)


def _is_valid_domain(domain: str) -> bool:
    """Return True if domain matches a simple hostname pattern."""
    return bool(_DOMAIN_RE.match(domain))


def _domain_allowed(netloc: str, base_netloc: str) -> bool:
    """
    Check whether the netloc is allowed.

    * If it matches the base domain, allow.
    * Otherwise, check against ALLOWED_DOMAINS.
    """
    # Strip port if present
    host = netloc.split(":")[0].lower()
    base_host = base_netloc.split(":")[0].lower()

    if host == base_host:
        return True

    # Compare without subdomains
    if host in ALLOWED_DOMAINS:
        return True

    # Allow subdomains of allowed domains (e.g., foo.trustedpartner.org)
    for allowed in ALLOWED_DOMAINS:
        if host.endswith("." + allowed):
            return True

    return False


def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL.

    Parameters
    ----------
    app_base_url : str
        Base authentication URL of the application (e.g., "https://app.example.com/auth").
    redirect_param : str
        User-supplied target URL or path (e.g., "/dashboard" or "https://evil.com").

    Returns
    -------
    str
        A fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe or malformed.
    """
    if not isinstance(app_base_url, str) or not isinstance(redirect_param, str):
        raise ValueError("Both arguments must be strings")

    # Parse the base URL
    parsed_base = urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("app_base_url must be a valid absolute URL")

    # Resolve the redirect target relative to the base
    resolved_url = urljoin(app_base_url, redirect_param)

    parsed_resolved = urlparse(resolved_url)
    if not parsed_resolved.scheme or not parsed_resolved.netloc:
        # The resolved URL is still relative or malformed
        raise ValueError("redirect_param could not be resolved to a valid absolute URL")

    # Ensure the scheme is HTTP or HTTPS
    if parsed_resolved.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_resolved.scheme}")

    # Validate domain
    if not _is_valid_domain(parsed_resolved.netloc.split(":")[0]):
        raise ValueError(f"Invalid domain in redirect URL: {parsed_resolved.netloc}")

    if not _domain_allowed(parsed_resolved.netloc, parsed_base.netloc):
        raise ValueError(
            f"Redirect URL domain '{parsed_resolved.netloc}' is not allowed"
        )

    # Reconstruct the URL to ensure it contains scheme, netloc and path
    safe_url = parsed_resolved.geturl()
    return safe_url


# Example usage:
if __name__ == "__main__":
    base = "https://app.example.com/auth"
    tests = [
        "/dashboard",
        "profile/edit",
        "https://app.example.com/settings",
        "https://trustedpartner.org/resource",
        "http://malicious.com/phish",
    ]

    for target in tests:
        try:
            print(f"Target: {target}\n=> {build_redirect_link(base, target)}\n")
        except ValueError as e:
            print(f"Target: {target}\n=> Error: {e}\n")