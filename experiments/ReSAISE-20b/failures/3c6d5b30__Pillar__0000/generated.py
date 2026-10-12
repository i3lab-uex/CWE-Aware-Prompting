import urllib.parse

# List of external domains that are considered safe for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    domain_base_url : str
        Base URL of the application (e.g., "https://myapp.com").
    next_redirect_param : str
        Desired redirect path or full URL provided by the user.

    Returns
    -------
    str
        A fully-qualified redirect URL that is either within the base domain
        or points to one of the allowed external domains.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or an allowed
        external domain.
    """
    if not isinstance(domain_base_url, str) or not isinstance(next_redirect_param, str):
        raise ValueError("Both arguments must be strings")

    # Normalize the base URL (remove trailing slash for consistency)
    base = domain_base_url.rstrip("/")
    parsed_base = urllib.parse.urlparse(base)

    # If the next_redirect_param looks like an absolute URL, parse it.
    parsed_next = urllib.parse.urlparse(next_redirect_param)

    if parsed_next.scheme and parsed_next.netloc:
        # Absolute URL: verify that the domain is allowed
        host = parsed_next.hostname.lower() if parsed_next.hostname else ""
        if not host:
            raise ValueError("Redirect URL must contain a hostname")

        # Allow the same domain as the base
        if host == parsed_base.hostname.lower():
            final_url = next_redirect_param
        # Allow any domain in the ALLOWED_DOMAINS list
        elif host in (d.lower() for d in ALLOWED_DOMAINS):
            final_url = next_redirect_param
        else:
            raise ValueError(f"Domain '{host}' is not permitted for redirection")
    else:
        # Treat as a relative path; ensure it starts with '/' to avoid
        # unintended file-system lookups or relative traversal.
        if not next_redirect_param.startswith("/"):
            raise ValueError("Relative redirect paths must start with '/'")

        # Build the full URL
        final_url = urllib.parse.urljoin(base + "/", next_redirect_param)

    # Final safety check: ensure the URL is still within the base domain
    parsed_final = urllib.parse.urlparse(final_url)
    if parsed_final.scheme not in ("http", "https"):
        raise ValueError("Redirect URL must use http or https scheme")

    final_host = parsed_final.hostname.lower() if parsed_final.hostname else ""
    base_host = parsed_base.hostname.lower() if parsed_base.hostname else ""

    if final_host != base_host and final_host not in (d.lower() for d in ALLOWED_DOMAINS):
        raise ValueError("Redirect URL is outside allowed domains")

    return final_url