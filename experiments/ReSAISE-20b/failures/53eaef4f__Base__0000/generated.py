import urllib.parse

# Domains that are explicitly allowed for external redirects.
SAFE_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add any additional safe domains here
]

def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Build a safe redirect URL from `next_path` relative to the application's
    base `primary_url`. The function ensures that the resulting URL does not
    point to an untrusted domain (CWE-601).

    Parameters:
        primary_url: The base URL of the application (e.g., "https://app.example.com").
        next_path: The user-specified redirect target. May be a relative path
                   ("/dashboard") or an absolute URL ("https://other.com/page").

    Returns:
        A fully-qualified redirect URL as a string.

    Raises:
        ValueError: If the final URL resolves to an untrusted domain or
                    if `next_path` contains malicious path traversal components.
    """
    # Normalize primary URL
    base = urllib.parse.urlparse(primary_url)
    if not base.scheme or not base.netloc:
        raise ValueError("primary_url must be a valid absolute URL")

    # Parse the user-provided next_path
    parsed_next = urllib.parse.urlparse(next_path)

    # If the user supplied an absolute URL
    if parsed_next.scheme and parsed_next.netloc:
        # Resolve against primary to handle relative URLs in the query component
        next_url = urllib.parse.urlunparse(parsed_next)
    else:
        # Relative path: ensure it starts with a single slash
        if not parsed_next.path.startswith("/"):
            raise ValueError("Relative redirect paths must start with '/'")
        # Prevent path traversal that escapes the base domain
        safe_path = urllib.parse.quote(parsed_next.path, safe="/")
        # Reconstruct the URL relative to primary
        next_url = urllib.parse.urljoin(primary_url, safe_path)

    # Parse the final URL to inspect its components
    final_parsed = urllib.parse.urlparse(next_url)

    # Ensure the scheme is HTTP or HTTPS
    if final_parsed.scheme not in {"http", "https"}:
        raise ValueError("Redirect URL must use HTTP or HTTPS scheme")

    # Check that the domain is either the same as primary_url or in SAFE_DOMAINS
    target_domain = final_parsed.hostname.lower() if final_parsed.hostname else ""
    base_domain = base.hostname.lower() if base.hostname else ""

    if target_domain != base_domain and target_domain not in {d.lower() for d in SAFE_DOMAINS}:
        raise ValueError(f"Redirect to untrusted domain '{target_domain}' is not allowed")

    # All checks passed; return the sanitized URL
    return next_url