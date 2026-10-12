#!/usr/bin/env python3
"""
Utility for building a safe redirect URI after login.

The function verifies that the requested `next_path` is either:
* a relative path within the same application, or
* an absolute URL whose domain is listed in SAFE_DOMAINS.

If the target fails these checks a ValueError is raised.
"""

from urllib.parse import urlparse, urljoin

# Domains that are explicitly allowed for redirection (e.g. third‑party services)
SAFE_DOMAINS = [
    "example.com",
    "trusted.example.org",
]

def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Build a safe redirect URL.

    Parameters
    ----------
    primary_url : str
        The base URL of the application (e.g. "https://app.example.com/").
    next_path : str
        The user supplied redirect target. Can be a relative path or an absolute URL.

    Returns
    -------
    str
        The fully qualified redirect URL that is guaranteed to be safe.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application domain or an allowed external domain.
    """
    if not primary_url:
        raise ValueError("primary_url must be a non-empty string")

    # Normalize the primary URL to avoid missing trailing slash
    base = primary_url.rstrip('/') + '/'

    # Parse the supplied next_path
    parsed_next = urlparse(next_path)

    if parsed_next.scheme and parsed_next.netloc:
        # Absolute URL: validate domain
        domain = parsed_next.netloc.split(':')[0]  # strip port if present
        if domain not in SAFE_DOMAINS:
            raise ValueError(f"Redirection to untrusted domain: {domain}")
        # Ensure the URL is absolute and uses http/https
        if parsed_next.scheme not in ('http', 'https'):
            raise ValueError(f"Unsupported URL scheme: {parsed_next.scheme}")
        redirect_url = next_path
    else:
        # Relative path: join with the base URL
        redirect_url = urljoin(base, next_path)

        # Verify that the resulting URL still points to our domain
        parsed_redirect = urlparse(redirect_url)
        base_parsed = urlparse(base)

        if parsed_redirect.netloc != base_parsed.netloc:
            raise ValueError(
                f"Redirect URL resolved to external domain: {parsed_redirect.netloc}"
            )

    # Final sanity check: the URL must be absolute
    final_parsed = urlparse(redirect_url)
    if not final_parsed.scheme or not final_parsed.netloc:
        raise ValueError("Redirect URL is malformed")

    return redirect_url

# Example usage
if __name__ == "__main__":
    try:
        print(build_redirect_uri("https://app.example.com/", "/dashboard"))
        print(build_redirect_uri("https://app.example.com/", "https://trusted.example.org/welcome"))
        # This will raise an exception
        print(build_redirect_uri("https://app.example.com/", "http://malicious.com/"))
    except ValueError as exc:
        print(f"Redirect error: {exc}")