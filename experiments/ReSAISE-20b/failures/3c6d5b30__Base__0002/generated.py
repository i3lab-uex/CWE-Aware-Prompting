import urllib.parse

# List of external domains that are allowed for redirects (example values)
ALLOWED_DOMAINS = [
    "trusted.com",
    "another-trusted.org",
]

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    domain_base_url : str
        The base URL of the application (e.g., "https://app.example.com").
    next_redirect_param : str
        The user-provided redirect target. May be a relative path or an absolute URL.

    Returns
    -------
    str
        A fully-qualified redirect URL that is safe to use.

    Raises
    ------
    ValueError
        If the resulting URL resolves to a domain that is neither the base domain nor an allowed external domain.
    """
    if not domain_base_url:
        raise ValueError("Base URL must be provided")

    # Parse the base URL once
    base_parsed = urllib.parse.urlparse(domain_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("Base URL must be a valid absolute URL")

    # Normalize the next redirect parameter
    next_parsed = urllib.parse.urlparse(next_redirect_param)

    # If the user supplied an absolute URL (scheme present)
    if next_parsed.scheme:
        # Validate that the host is either the same as base or in ALLOWED_DOMAINS
        host = next_parsed.netloc.lower()
        if host != base_parsed.netloc.lower() and host not in ALLOWED_DOMAINS:
            raise ValueError(f"Redirect target '{next_redirect_param}' is not allowed")
        # Return the user-supplied absolute URL unchanged (but parsed to ensure it's valid)
        return urllib.parse.urlunparse(next_parsed)

    # If the user supplied a relative path (no scheme), construct full URL
    if not next_redirect_param.startswith("/"):
        # Treat any relative path as starting with a slash
        next_redirect_param = "/" + next_redirect_param

    # Use urljoin to correctly combine base and relative path
    full_url = urllib.parse.urljoin(domain_base_url, next_redirect_param)

    # Final sanity check: ensure the resulting URL's domain is safe
    final_parsed = urllib.parse.urlparse(full_url)
    if final_parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {final_parsed.scheme}")

    host = final_parsed.netloc.lower()
    if host != base_parsed.netloc.lower() and host not in ALLOWED_DOMAINS:
        raise ValueError(f"Redirect target '{full_url}' is not allowed")

    return full_url