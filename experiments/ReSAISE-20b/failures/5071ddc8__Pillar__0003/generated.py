import urllib.parse

# Example list of allowed external domains. In a real application this would be configured elsewhere.
ALLOWED_DOMAINS = {"example.com", "trustedpartner.org"}

def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Construct a safe redirect URL after authentication.

    Parameters
    ----------
    main_base_url : str
        The base URL of the application (e.g., "https://myapp.com/").
    next_route : str
        The user‑supplied path or full URL to redirect to.

    Returns
    -------
    str
        The fully resolved, safe redirect URL.

    Raises
    ------
    ValueError
        If the constructed URL is not within the same origin as ``main_base_url``
        or does not belong to an allowed external domain.
    """
    # Parse the base URL once
    base_parsed = urllib.parse.urlparse(main_base_url)

    # Resolve the next route against the base URL
    resolved = urllib.parse.urljoin(main_base_url, next_route)
    parsed_resolved = urllib.parse.urlparse(resolved)

    # If the resolved URL is relative (no netloc), it's safe
    if not parsed_resolved.netloc:
        return resolved

    # Check that the scheme is HTTP or HTTPS
    if parsed_resolved.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed_resolved.scheme}")

    # Same‑origin check (including port if specified)
    same_origin = (
        parsed_resolved.scheme == base_parsed.scheme and
        parsed_resolved.netloc.lower() == base_parsed.netloc.lower()
    )
    if same_origin:
        return resolved

    # If not same origin, ensure the host is in the allowed list
    host = parsed_resolved.hostname.lower() if parsed_resolved.hostname else ""
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Redirect target '{host}' is not allowed")

    # Finally, return the resolved URL
    return resolved

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(assemble_redirect_uri("https://myapp.com/", "/dashboard"))
#     print(assemble_redirect_uri("https://myapp.com/", "https://example.com/landing"))
#     # This will raise ValueError
#     # print(assemble_redirect_uri("https://myapp.com/", "https://malicious.com/"))