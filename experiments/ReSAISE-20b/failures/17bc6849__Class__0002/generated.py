import urllib.parse

# Example list of domains that are considered safe for external redirects.
ALLOWED_DOMAINS = {"example.com", "trustedpartner.org"}

def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    app_home_url : str
        Base URL of the application (e.g., "https://app.example.com/").
    forward_param : str
        User-provided path or URL to redirect to.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is outside the base domain and not in ALLOWED_DOMAINS.
    """
    # Normalise the application home URL
    base = urllib.parse.urlparse(app_home_url)
    if not base.scheme or not base.netloc:
        raise ValueError("app_home_url must be a fully-qualified URL")

    # Parse the forward parameter
    parsed_forward = urllib.parse.urlparse(forward_param)

    # If it's a relative path, simply join it to the base URL
    if not parsed_forward.scheme and not parsed_forward.netloc:
        # Ensure it starts with a slash to avoid ambiguous joins
        path = parsed_forward.path or "/"
        if not path.startswith("/"):
            path = "/" + path
        full_url = urllib.parse.urljoin(app_home_url, path)
    else:
        # It's an absolute URL; validate its domain
        forward_netloc = parsed_forward.netloc.lower()
        base_netloc = base.netloc.lower()

        # Allow if it matches the app's domain
        if forward_netloc == base_netloc:
            full_url = urllib.parse.urlunparse(parsed_forward)
        # Or if it is in the list of externally allowed domains
        elif any(forward_netloc.endswith("." + d) or forward_netloc == d for d in ALLOWED_DOMAINS):
            full_url = urllib.parse.urlunparse(parsed_forward)
        else:
            raise ValueError(
                f"Redirect URL '{forward_param}' is not allowed: domain '{forward_netloc}' "
                "is outside the application and not in ALLOWED_DOMAINS."
            )

    # Final sanity check: ensure that the resulting URL starts with the base scheme
    final_parsed = urllib.parse.urlparse(full_url)
    if not final_parsed.scheme or not final_parsed.netloc:
        raise ValueError("Resulting redirect URL is malformed")

    return full_url