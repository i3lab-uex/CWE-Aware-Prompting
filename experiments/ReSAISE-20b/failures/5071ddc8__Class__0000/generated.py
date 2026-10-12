#!/usr/bin/env python3
"""
Utility to safely construct a post‑login redirect URL.

The function ensures that the resulting URL is either:
* a relative path within the same application domain, or
* an absolute URL whose host is listed in ``ALLOWED_DOMAINS``.
"""

from urllib.parse import urlparse, urljoin
from typing import List

# Example list of approved external domains.
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
    # Add additional domains as needed.
]


def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Resolve the user's desired post‑login destination.

    Parameters
    ----------
    main_base_url : str
        The base URL of the application (e.g., "https://app.example.com").
    next_route : str
        The user‑supplied path or full URL to redirect to.

    Returns
    -------
    str
        The fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe (outside the base domain and not in
        ``ALLOWED_DOMAINS``).
    """
    # Parse the base URL to extract its scheme and network location.
    base_parsed = urlparse(main_base_url)
    if not (base_parsed.scheme and base_parsed.netloc):
        raise ValueError(f"Invalid main_base_url: {main_base_url!r}")

    # Resolve the next_route against the base URL.
    # urljoin handles both relative paths and absolute URLs.
    resolved = urljoin(main_base_url, next_route)

    # Parse the resolved URL to inspect its components.
    resolved_parsed = urlparse(resolved)

    # If the scheme is missing (e.g., user passed a relative path without leading slash),
    # prepend the base scheme to avoid mis‑interpretation.
    if not resolved_parsed.scheme:
        resolved = f"{base_parsed.scheme}://{resolved}"
        resolved_parsed = urlparse(resolved)

    # Check if the URL points to an external domain.
    host_is_external = resolved_parsed.netloc.lower() != base_parsed.netloc.lower()

    if host_is_external:
        # External URLs must be explicitly allowed.
        host = resolved_parsed.netloc.split(":")[0].lower()  # strip port if present
        if host not in (d.lower() for d in ALLOWED_DOMAINS):
            raise ValueError(
                f"Redirect to external host {host!r} is not permitted."
            )

    # Ensure the resolved URL uses HTTPS to avoid leaking credentials.
    if resolved_parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {resolved_parsed.scheme!r}")

    # Normalise the URL to avoid double slashes and other anomalies.
    safe_url = resolved_parsed.geturl()

    return safe_url


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    base = "https://app.example.com"
    # Relative path
    print(assemble_redirect_uri(base, "/dashboard"))
    # Absolute URL to allowed domain
    print(assemble_redirect_uri(base, "https://example.com/welcome"))
    # Absolute URL to disallowed domain (raises ValueError)
    try:
        print(assemble_redirect_uri(base, "https://malicious.com/hack"))
    except ValueError as exc:
        print(f"Blocked redirect: {exc}")