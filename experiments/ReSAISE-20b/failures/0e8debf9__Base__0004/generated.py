import urllib.parse
from typing import List

# Pre-approved external domains for redirection (example)
ALLOWED_DOMAINS: List[str] = [
    "trusted.com",
    "anothertrusteddomain.org",
]

def _is_domain_allowed(domain: str) -> bool:
    """Check if a domain is in the allowed list (case‑insensitive)."""
    return any(domain.lower() == d.lower() for d in ALLOWED_DOMAINS)

def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    auth_base_url : str
        The base authentication URL of the application (e.g. "https://app.example.com").
    post_login_param : str
        The URL path or full URL supplied by the user to redirect to after login.

    Returns
    -------
    str
        The resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an untrusted domain or is otherwise unsafe.
    """
    # Parse base URL once
    base_parsed = urllib.parse.urlparse(auth_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError(f"Invalid auth_base_url: {auth_base_url!r}")

    # Resolve the user supplied parameter against the base URL
    resolved = urllib.parse.urljoin(auth_base_url, post_login_param)

    # Parse the resulting URL to inspect its components
    resolved_parsed = urllib.parse.urlparse(resolved)

    # Ensure the URL is absolute (has a scheme) after resolution
    if not resolved_parsed.scheme:
        # If the user supplied a relative path, prepend scheme/host from base
        resolved_parsed = resolved_parsed._replace(
            scheme=base_parsed.scheme,
            netloc=base_parsed.netloc
        )
        resolved = urllib.parse.urlunparse(resolved_parsed)

    # Check that the host is either the same as auth_base_url or in ALLOWED_DOMAINS
    target_host = resolved_parsed.hostname
    if not target_host:
        raise ValueError("Redirect URL does not contain a hostname")

    # Normalize hosts for comparison
    base_host = base_parsed.hostname.lower()
    target_host_lower = target_host.lower()

    if target_host_lower != base_host and not _is_domain_allowed(target_host_lower):
        raise ValueError(
            f"Unsafe redirect target: {target_host!r} is not allowed"
        )

    # Optional: Ensure that the path is not pointing to a different sub‑domain of
    # auth_base_url (e.g., https://malicious.example.com). The check above
    # already covers this by comparing hostname equality.

    return resolved

# Example usage:
if __name__ == "__main__":
    base = "https://app.example.com/login"
    # Safe relative path
    print(generate_redirect_uri(base, "/dashboard"))
    # Safe external domain
    print(generate_redirect_uri(base, "https://trusted.com/welcome"))
    # Unsafe external domain (will raise ValueError)
    try:
        print(generate_redirect_uri(base, "https://evil.com/phish"))
    except ValueError as e:
        print("Caught error:", e)