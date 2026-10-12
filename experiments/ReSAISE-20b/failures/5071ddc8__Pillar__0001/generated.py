import urllib.parse

# Pre-approved external domains that may be used for redirection.
ALLOWED_DOMAINS = {"example.com", "trusted.org"}

def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Build a safe redirect URL after authentication.

    Parameters
    ----------
    main_base_url : str
        The base URL of the application (e.g. "https://app.example.com/").
    next_route : str
        The path or full URL the user wants to navigate to after login.

    Returns
    -------
    str
        The fully resolved, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL points to an unsafe domain.
    """
    # Resolve the next_route against the base URL
    resolved = urllib.parse.urljoin(main_base_url, next_route)

    # Parse the resulting URL
    parsed = urllib.parse.urlparse(resolved)

    # Ensure scheme is present (http or https)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Extract the host (netloc may contain port)
    host = parsed.hostname
    if not host:
        # If hostname is missing, the URL might be relative; treat as safe
        return resolved

    # Normalize host for comparison (lowercase)
    host = host.lower()

    # Determine the base domain of main_base_url
    base_parsed = urllib.parse.urlparse(main_base_url)
    base_host = base_parsed.hostname.lower() if base_parsed.hostname else ""

    # Allow the URL if it is under the same domain (including subdomains)
    def is_subdomain(child: str, parent: str) -> bool:
        return child == parent or child.endswith("." + parent)

    if is_subdomain(host, base_host):
        return resolved

    # Allow the URL if it is in the list of explicitly allowed domains
    if host in ALLOWED_DOMAINS:
        return resolved

    # If none of the above, raise an error
    raise ValueError(f"Unsafe redirect target: {resolved}")