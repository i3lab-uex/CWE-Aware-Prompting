#!/usr/bin/env python3
"""
Secure redirect URL builder.

This module provides a single function, ``build_redirect_uri``, which
constructs a redirect URL from a base application URL and a user‑supplied
``next_path`` value.  The function protects against open redirect
vulnerabilities (CWE‑610) by ensuring that the resulting URL resolves to
the application’s own domain or to one of a set of explicitly allowed
external domains.

Author: OpenAI ChatGPT
"""

from urllib.parse import urlparse, urljoin

# --------------------------------------------------------------------------- #
# Allowed external domains.  Add any domain you consider safe for redirection.
# --------------------------------------------------------------------------- #
SAFE_DOMAINS = [
    "example.com",     # Replace with your trusted domains
    "trustedpartner.org",
]

def _normalize_domain(domain: str) -> str:
    """
    Normalise a domain for comparison.

    Lower‑case and strip leading ``www.`` if present.
    """
    domain = domain.lower()
    return domain[4:] if domain.startswith("www.") else domain

def _is_allowed_domain(target_netloc: str, base_netloc: str) -> bool:
    """
    Return True if ``target_netloc`` is either the same as ``base_netloc``
    or appears in ``SAFE_DOMAINS``.
    """
    target_norm = _normalize_domain(target_netloc)
    base_norm = _normalize_domain(base_netloc)

    if target_norm == base_norm:
        return True

    for domain in SAFE_DOMAINS:
        if target_norm == _normalize_domain(domain):
            return True

    return False


def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Build a safe redirect URL.

    Parameters
    ----------
    primary_url : str
        The base application URL (e.g. ``https://app.example.com``).
    next_path : str
        The user‑supplied path or URL that the user wishes to visit after login.

    Returns
    -------
    str
        A fully resolved redirect URL that is guaranteed to point either back
        into the application or to one of the domains listed in ``SAFE_DOMAINS``.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is not permitted.
    """
    # Parse base URL and validate it has scheme/netloc
    base_parsed = urlparse(primary_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid primary URL: {primary_url!r}")

    # Resolve the next path against the base URL
    joined = urljoin(primary_url, next_path)

    # Parse the resolved URL to inspect its components
    target_parsed = urlparse(joined)

    # Ensure the scheme is http or https; otherwise reject
    if target_parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {target_parsed.scheme!r}")

    # Validate that the domain is allowed
    if not _is_allowed_domain(target_parsed.netloc, base_parsed.netloc):
        raise ValueError(
            f"Redirect target domain {target_parsed.netloc!r} is not allowed"
        )

    # Return the fully resolved, safe URL
    return joined


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        print(build_redirect_uri("https://app.example.com", "/dashboard"))
        print(build_redirect_uri("https://app.example.com", "https://trustedpartner.org/welcome"))
        # The following will raise ValueError
        print(build_redirect_uri("https://app.example.com", "https://malicious.net/phish"))
    except ValueError as exc:
        print(f"Redirect rejected: {exc}")