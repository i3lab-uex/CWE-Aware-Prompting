import urllib.parse

# Example allowed external domains – in a real app this would be configurable.
ALLOWED_DOMAINS = {"example.com", "trusted.org"}

def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g. "https://myapp.com/").
    redirect_param : str
        The user-provided redirect target. It may be a relative path or an absolute URL.

    Returns
    -------
    str
        The fully-qualified redirect URL that is guaranteed to be either:
          * Within the same host as `app_base_url`, or
          * An absolute URL whose hostname is in ALLOWED_DOMAINS.

    Raises
    ------
    ValueError
        If the redirect target resolves to a host that is not allowed.
    """
    # Normalise base URL
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("app_base_url must be a valid absolute URL")

    # Parse the redirect parameter
    parsed_redirect = urllib.parse.urlparse(redirect_param)

    # Case 1: redirect is relative – simply join it to the base URL
    if not parsed_redirect.scheme and not parsed_redirect.netloc:
        # Join relative path to base URL
        joined = urllib.parse.urljoin(app_base_url, redirect_param)
        # Validate that the joined URL stays within the same host
        parsed_joined = urllib.parse.urlparse(joined)
        if parsed_joined.netloc != parsed_base.netloc:
            raise ValueError("Relative redirect resolved to a different host")
        return joined

    # Case 2: redirect is absolute – check hostname against allowed list
    host = parsed_redirect.hostname or ""
    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Redirect host '{host}' is not allowed")

    # Ensure the scheme is HTTP or HTTPS
    if parsed_redirect.scheme not in ("http", "https"):
        raise ValueError("Redirect scheme must be http or https")

    # Reconstruct the URL to avoid fragments or query parameters that might lead
    # to unexpected side‑effects. Preserve path, params, query, and fragment if needed.
    safe_redirect = urllib.parse.urlunparse((
        parsed_redirect.scheme,
        parsed_redirect.netloc,
        parsed_redirect.path,
        parsed_redirect.params,
        parsed_redirect.query,
        parsed_redirect.fragment
    ))
    return safe_redirect

# Example usage:
if __name__ == "__main__":
    try:
        print(generate_redirect_link("https://myapp.com/", "/dashboard"))
        print(generate_redirect_link("https://myapp.com/", "https://example.com/welcome"))
    except ValueError as e:
        print(f"Redirect error: {e}")