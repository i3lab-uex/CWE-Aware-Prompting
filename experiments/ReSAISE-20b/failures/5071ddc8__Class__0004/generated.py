import urllib.parse

# Pre‑approved external domains for redirects
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.org",
}

def _is_same_origin(base: str, target: str) -> bool:
    """
    Return True if `target` has the same scheme and netloc as `base`.
    """
    base_parsed = urllib.parse.urlparse(base)
    target_parsed = urllib.parse.urlparse(target)

    # If target is relative, it's safe
    if not target_parsed.scheme and not target_parsed.netloc:
        return True

    # Compare scheme and netloc (including port)
    return (
        base_parsed.scheme == target_parsed.scheme
        and base_parsed.netloc.lower() == target_parsed.netloc.lower()
    )

def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Build a safe redirect URI.

    Parameters
    ----------
    main_base_url : str
        The base URL of the application (e.g. "https://app.example.com/").
    next_route : str
        The URL or path the user wants to go after login.

    Returns
    -------
    str
        A fully resolved redirect URL that is safe to use.

    Raises
    ------
    ValueError
        If the resulting URL resolves outside of the base domain and is not in ALLOWED_DOMAINS.
    """
    if not main_base_url:
        raise ValueError("main_base_url must be provided")

    # Normalize the base URL
    base_parsed = urllib.parse.urlparse(main_base_url.rstrip("/"))
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("main_base_url must be a valid absolute URL")

    # Resolve next_route against the base
    resolved = urllib.parse.urljoin(main_base_url, next_route)

    # Parse the resolved URL
    resolved_parsed = urllib.parse.urlparse(resolved)

    # If same origin, we are good
    if _is_same_origin(main_base_url, resolved):
        return resolved

    # If not same origin, check against allowed domains
    target_netloc = resolved_parsed.netloc.lower()
    # Remove port for domain comparison
    host, _, _ = target_netloc.partition(":")
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Redirect to unapproved domain: {host}")

    # All checks passed
    return resolved

# Example usage (for testing only)
if __name__ == "__main__":
    try:
        print(assemble_redirect_uri("https://app.example.com/", "/dashboard"))
        print(assemble_redirect_uri("https://app.example.com/", "https://trusted.org/welcome"))
        # This will raise ValueError
        print(assemble_redirect_uri("https://app.example.com/", "https://evil.com/hack"))
    except ValueError as e:
        print("Redirect rejected:", e)