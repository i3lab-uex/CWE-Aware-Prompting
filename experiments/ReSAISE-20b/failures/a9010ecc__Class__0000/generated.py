import urllib.parse

# List of external domains that are considered safe for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]


def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    app_base_url : str
        The base URL of the application (e.g., "https://myapp.com").
    redirect_param : str
        The user supplied path or URL to redirect to after login.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application domain or
        if it points to an external domain that is not in ALLOWED_DOMAINS.
    """
    # Parse the base URL once
    base_parsed = urllib.parse.urlparse(app_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("app_base_url must be a valid absolute URL")

    # Parse the redirect parameter
    redirect_parsed = urllib.parse.urlparse(redirect_param)

    # If redirect has a scheme and netloc, it's an absolute URL
    if redirect_parsed.scheme in ("http", "https") and redirect_parsed.netloc:
        # Normalize the netloc for comparison (case-insensitive)
        target_netloc = redirect_parsed.netloc.lower()

        # Check if the target domain is allowed
        if target_netloc not in [d.lower() for d in ALLOWED_DOMAINS]:
            raise ValueError(f"Redirect to domain '{target_netloc}' is not allowed")

        # Construct the final URL (preserve scheme, netloc, path, params, query, fragment)
        final_url = urllib.parse.urlunparse(redirect_parsed)

    else:
        # Treat redirect_param as a relative path
        # Join it with the base URL
        joined = urllib.parse.urljoin(app_base_url, redirect_param)

        # Parse the joined URL to verify it remains within the base domain
        joined_parsed = urllib.parse.urlparse(joined)

        if joined_parsed.netloc.lower() != base_parsed.netloc.lower():
            raise ValueError(
                f"Redirect path '{redirect_param}' resolves to an external domain "
                f"('{joined_parsed.netloc}') which is not allowed"
            )

        final_url = joined

    return final_url