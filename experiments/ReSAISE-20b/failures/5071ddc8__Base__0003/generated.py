import urllib.parse

# List of external domains that are explicitly allowed for redirection.
ALLOWED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    # add more domains as needed
}


def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Build a safe redirect URL by combining the application's base URL with
    the user supplied `next_route`. The function ensures that the resulting
    URL is either a relative path within the application or an absolute URL
    pointing to one of the allowed external domains.

    Parameters
    ----------
    main_base_url : str
        Base URL of the application (e.g. "https://app.example.com").
    next_route : str
        User supplied path or full URL to redirect to after login.

    Returns
    -------
    str
        A fully resolved, safe URL for redirection.

    Raises
    ------
    ValueError
        If `next_route` resolves to a URL outside the application domain and
        not in the list of allowed external domains.
    """
    # Parse the base URL once
    base_parts = urllib.parse.urlparse(main_base_url)
    if not base_parts.scheme or not base_parts.netloc:
        raise ValueError("Invalid main_base_url")

    # Parse the user supplied route
    next_parts = urllib.parse.urlparse(next_route)

    if next_parts.scheme and next_parts.netloc:
        # Absolute URL supplied by the user
        netloc = next_parts.netloc.lower()

        # If the absolute URL is within the same host as the base, it's safe
        if netloc == base_parts.netloc.lower():
            # Reconstruct the URL to avoid fragments or query manipulation
            safe_url = urllib.parse.urlunparse(
                (next_parts.scheme, netloc,
                 next_parts.path or "",
                 "",  # no params
                 next_parts.query, "")
            )
        else:
            # Check against the allowed domains list (case‑insensitive)
            host = netloc.split(":")[0]  # strip port if present
            if host.lower() not in {d.lower() for d in ALLOWED_DOMAINS}:
                raise ValueError(f"Redirect to external domain '{host}' is not allowed")
            # Allow the absolute URL as it matches an approved domain
            safe_url = urllib.parse.urlunparse(next_parts._replace(fragment=""))
    else:
        # Relative path: join it with the base URL
        safe_url = urllib.parse.urljoin(main_base_url, next_route)

    # Final safety check: ensure the resulting URL starts with the base scheme
    final_parts = urllib.parse.urlparse(safe_url)
    if final_parts.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {final_parts.scheme}")

    return safe_url