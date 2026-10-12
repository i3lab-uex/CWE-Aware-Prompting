import urllib.parse

# Example list of allowed external domains (should be configured per deployment)
ALLOWED_DOMAINS = {"example.com", "trusted.org"}

def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL after authentication.

    Parameters
    ----------
    app_base_url : str
        Base URL of the application (e.g., "https://app.example.com/login").
    redirect_param : str
        The target URL supplied by the user (can be a path or full URL).

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe (outside allowed domains or invalid scheme).
    """
    if not app_base_url:
        raise ValueError("app_base_url must be provided")

    # Normalize the base URL
    parsed_base = urllib.parse.urlparse(app_base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("app_base_url must be a valid absolute URL")

    # Trim whitespace from redirect_param
    redirect_param = redirect_param.strip()

    # If the user supplied a relative path, simply join it with the base
    if not urllib.parse.urlparse(redirect_param).netloc:
        # Prevent directory traversal by normalizing the path
        safe_path = urllib.parse.urljoin("/", redirect_param)
        resolved_url = urllib.parse.urlunparse(
            (
                parsed_base.scheme,
                parsed_base.netloc,
                safe_path,
                "",  # params
                "",  # query
                "",  # fragment
            )
        )
        return resolved_url

    # The user supplied an absolute URL – validate it
    parsed_redirect = urllib.parse.urlparse(redirect_param)

    # Ensure scheme is http or https
    if parsed_redirect.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed_redirect.scheme}")

    # Allow if the host matches the app's base domain
    if parsed_redirect.netloc == parsed_base.netloc:
        return redirect_param

    # Allow if the host is in ALLOWED_DOMAINS
    host = parsed_redirect.netloc.split(":")[0]  # strip port if present
    if host.lower() in (d.lower() for d in ALLOWED_DOMAINS):
        return redirect_param

    # If we reach here, the URL is considered unsafe
    raise ValueError(f"Redirect to external domain '{host}' is not permitted")