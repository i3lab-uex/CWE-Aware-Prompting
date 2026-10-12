import urllib.parse

# Pre‑approved external domains that may be used for redirection.
ALLOWED_DOMAINS = {
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed.
}

def assemble_redirect_uri(main_base_url: str, next_route: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    main_base_url : str
        Base authentication URL of the application (e.g. "https://app.example.com/auth").
    next_route : str
        The path or full URL the user wishes to visit after login.

    Returns
    -------
    str
        A fully qualified, safe redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe: external domain not in ALLOWED_DOMAINS,
        or an unsupported scheme is used.
    """
    # Parse the base URL to get its components
    base_parsed = urllib.parse.urlparse(main_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("Invalid main_base_url")

    # Resolve the next route relative to the base URL
    resolved = urllib.parse.urljoin(base_parsed.geturl(), next_route)

    # Parse the resolved URL to inspect its components
    target = urllib.parse.urlparse(resolved)

    # Ensure the scheme is http or https (or whatever your app supports)
    if target.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {target.scheme}")

    # Determine if the target is relative (no netloc) or absolute
    if not target.netloc:
        # Relative path – safe by definition, just return it
        return urllib.parse.urlunparse(
            target._replace(scheme=base_parsed.scheme, netloc=base_parsed.netloc)
        )

    # Absolute URL – verify that the domain is allowed
    target_domain = target.hostname.lower() if target.hostname else ""
    base_domain   = base_parsed.hostname.lower() if base_parsed.hostname else ""

    # Allow same‑site redirects
    if target_domain == base_domain:
        return resolved

    # Or allow external domains that are explicitly permitted
    if target_domain in ALLOWED_DOMAINS:
        return resolved

    # Anything else is disallowed
    raise ValueError(f"Redirect to untrusted domain: {target_domain}")