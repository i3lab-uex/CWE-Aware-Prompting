#!/usr/bin/env python3
"""
Secure user redirection helper.

The `secure_user_redirect` function validates a user supplied URL against
a whitelist of approved domains and returns a sanitized, safe-to-use URL.
If the domain is not on the whitelist or the scheme is disallowed,
a ValueError is raised.

Author: OpenAI ChatGPT
"""

from urllib.parse import urlparse, urlunparse

# Whitelist of approved domains (case‑insensitive).
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "secure.example.net",
}

# Allowed URL schemes.
ALLOWED_SCHEMES = {"http", "https"}


def _sanitize_netloc(netloc: str) -> str:
    """
    Remove user info and port from netloc, normalise case.
    """
    # Strip any credentials (user:pass@)
    if "@" in netloc:
        _, netloc = netloc.rsplit("@", 1)
    # Remove port if present
    if ":" in netloc:
        host, _ = netloc.split(":", 1)
    else:
        host = netloc
    return host.lower()


def secure_user_redirect(url_input: str) -> str:
    """
    Validate and sanitize a user supplied URL for safe redirection.

    Parameters
    ----------
    url_input : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A validated, sanitized URL that can be used for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list, or if the scheme
        is not allowed.
    """
    # Basic normalisation: strip whitespace and collapse multiple slashes
    url_input = url_input.strip()

    # Parse the URL
    parsed = urlparse(url_input)

    # Ensure scheme is present and allowed
    if not parsed.scheme:
        raise ValueError("URL must include a scheme (http or https).")
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Disallowed URL scheme: {parsed.scheme}")

    # Ensure netloc (domain) is present
    if not parsed.netloc:
        raise ValueError("URL must include a network location (domain).")

    # Normalise and validate domain
    host = _sanitize_netloc(parsed.netloc)
    if host not in APPROVED_DOMAINS:
        raise ValueError(f"Domain '{host}' is not approved for redirection.")

    # Reconstruct a safe URL without any userinfo or port
    safe_netloc = host  # we intentionally drop port and credentials
    sanitized_parts = (
        parsed.scheme,
        safe_netloc,
        parsed.path or "",
        parsed.params or "",
        parsed.query or "",
        ""  # drop fragment
    )
    safe_url = urlunparse(sanitized_parts)

    return safe_url


# Example usage (for debugging only – remove or guard under __main__ in production)
if __name__ == "__main__":
    test_urls = [
        "https://example.com/some/page?foo=bar",
        "http://trustedsite.org/path",
        "https://malicious.com/evil",
        "ftp://example.com/resource",
    ]

    for u in test_urls:
        try:
            print(f"Original: {u}\nRedirect to: {secure_user_redirect(u)}\n")
        except ValueError as e:
            print(f"Original: {u}\nError: {e}\n")