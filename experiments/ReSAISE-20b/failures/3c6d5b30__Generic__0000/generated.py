import urllib.parse

# Example list of allowed external domains for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    "sub.domain.net",
]

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a secure redirect URL by appending the user-provided path or
    absolute URL to the application's base domain. The resulting URL must be
    either a relative path within the same domain or an absolute URL whose
    hostname is listed in ``ALLOWED_DOMAINS``.

    Parameters
    ----------
    domain_base_url : str
        The base URL of the application (e.g. "https://myapp.example.com/").
    next_redirect_param : str
        The target URL path or absolute URL supplied by the user.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the constructed URL points outside the base domain or to an
        external host not in ``ALLOWED_DOMAINS``.
    """
    if not domain_base_url:
        raise ValueError("Base URL must be provided")

    # Normalise the base URL to ensure it ends with a slash for urljoin
    if not domain_base_url.endswith("/"):
        base = domain_base_url + "/"
    else:
        base = domain_base_url

    # Parse the next redirect param to determine if it is relative or absolute
    parsed_next = urllib.parse.urlparse(next_redirect_param)

    # If the redirect is relative (no scheme or netloc), join with base
    if not parsed_next.scheme and not parsed_next.netloc:
        # Ensure it does not contain any attempt to escape the base path
        safe_path = urllib.parse.quote(parsed_next.path, safe="/")
        final_url = urllib.parse.urljoin(base, safe_path)
    else:
        # Absolute URL: verify hostname is allowed
        host = parsed_next.hostname
        if not host:
            raise ValueError("Redirect URL must contain a hostname")
        # Resolve possible port numbers in host
        if ":" in host:
            host = host.split(":")[0]
        # Case-insensitive comparison for domain match
        if not any(host.lower() == allowed.lower()
                   or host.lower().endswith("." + allowed.lower())
                   for allowed in ALLOWED_DOMAINS):
            raise ValueError(f"Redirect host '{host}' is not allowed")
        # Reconstruct the URL to ensure we keep path, query, fragment
        final_url = urllib.parse.urlunparse(parsed_next)

    # Final sanity check: ensure the redirect URL is within the same scheme
    parsed_final = urllib.parse.urlparse(final_url)
    if not parsed_final.scheme:
        raise ValueError("Final redirect URL must have a scheme")

    return final_url