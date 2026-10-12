import urllib.parse

# Example allowed external domains (should be defined elsewhere in your project)
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    "myapp.example.net",
]

def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Build a safe redirect URL after login.

    Parameters
    ----------
    app_home_url : str
        The base URL of the application (e.g. "https://myapp.com/").
    forward_param : str
        The URL path or address supplied by the user.

    Returns
    -------
    str
        A fully-qualified redirect URL that is either relative to the
        application or an externally allowed domain.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application domain or an
        explicitly allowed external domain.
    """
    # Ensure the base URL ends with a slash for proper joining
    if not app_home_url.endswith("/"):
        app_home_url += "/"

    # Parse the forward parameter
    parsed_forward = urllib.parse.urlparse(forward_param)

    # If the user supplied a relative path, simply join it with the app base URL
    if not parsed_forward.scheme and not parsed_forward.netloc:
        # Join while preserving query & fragment
        safe_path = urllib.parse.urljoin(app_home_url, parsed_forward.path)
        # Append any query or fragment from the original forward_param
        if parsed_forward.query:
            safe_path += f"?{parsed_forward.query}"
        if parsed_forward.fragment:
            safe_path += f"#{parsed_forward.fragment}"
        return safe_path

    # If an absolute URL is supplied, validate its domain
    forward_domain = parsed_forward.netloc.lower()
    app_parsed = urllib.parse.urlparse(app_home_url)
    app_domain = app_parsed.netloc.lower()

    # Allowed if it matches the application domain or is in ALLOWED_DOMAINS
    if forward_domain == app_domain or forward_domain in {d.lower() for d in ALLOWED_DOMAINS}:
        # Reconstruct the URL to ensure consistent formatting
        return urllib.parse.urlunparse(parsed_forward)

    raise ValueError(
        f"Redirect target '{forward_param}' is not allowed. "
        "Only relative URLs or domains in ALLOWED_DOMAINS are permitted."
    )