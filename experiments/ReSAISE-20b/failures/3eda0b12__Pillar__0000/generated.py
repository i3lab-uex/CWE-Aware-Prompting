#!/usr/bin/env python3
"""
Secure construction of a post‑login redirect URL.

The function validates that the target location is either:
  • A relative path within the application.
  • An absolute URL that points to the same host as `main_url`.
  • An absolute URL whose host is listed in `PERMITTED_DOMAINS`.

If the target does not satisfy any of these conditions a ValueError
is raised to prevent open‑redirect attacks.

Author: OpenAI ChatGPT
"""

from urllib.parse import urlparse, urljoin
from typing import List

# Domains that are explicitly allowed for external redirects.
PERMITTED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]

def construct_redirect_url(main_url: str, target_param: str) -> str:
    """
    Build a safe redirect URL.

    Parameters
    ----------
    main_url : str
        The base application URL (e.g., "https://app.example.com/").
    target_param : str
        The user supplied redirect target, which may be a relative path,
        an absolute URL, or a query string.

    Returns
    -------
    str
        The fully qualified redirect URL that is guaranteed to stay within
        the application domain or one of the permitted external domains.

    Raises
    ------
    ValueError
        If `target_param` resolves to a location outside the allowed
        domains or is otherwise unsafe.
    """
    # Parse the base URL to extract its components.
    main_parsed = urlparse(main_url)
    if not main_parsed.scheme or not main_parsed.netloc:
        raise ValueError(f"Invalid base URL: {main_url!r}")

    # Resolve the target against the base URL.
    resolved = urljoin(main_url, target_param)

    # Parse the resolved URL to inspect its components.
    parsed = urlparse(resolved)

    # Allow absolute URLs that match the main host or are in permitted domains.
    if parsed.scheme and parsed.netloc:
        # Normalize the hostname (case-insensitive per RFC).
        host = parsed.hostname.lower()
        if host == main_parsed.hostname.lower():
            return resolved
        if host in {d.lower() for d in PERMITTED_DOMAINS}:
            return resolved
        raise ValueError(f"Redirect to disallowed domain: {host!r}")

    # For relative URLs, ensure they do not escape the application root.
    if parsed.path.startswith("/"):
        # Normalise path to prevent traversal attacks (e.g., "/../secret").
        normalized_path = "/" + "/".join(
            part for part in parsed.path.split("/") if part and part != ".."
        )
        # Reconstruct the URL without query or fragment for safety.
        safe_url = f"{main_parsed.scheme}://{main_parsed.netloc}{normalized_path}"
        if parsed.query:
            safe_url += f"?{parsed.query}"
        if parsed.fragment:
            safe_url += f"#{parsed.fragment}"
        return safe_url

    # If we reach here, the target is ambiguous or unsafe.
    raise ValueError(f"Invalid redirect target: {target_param!r}")

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     try:
#         print(construct_redirect_url("https://app.example.com/", "/dashboard"))
#         print(construct_redirect_url("https://app.example.com/", "https://example.com/home"))
#         print(construct_redirect_url("https://app.example.com/", "https://malicious.com/"))
#     except ValueError as e:
#         print(e)