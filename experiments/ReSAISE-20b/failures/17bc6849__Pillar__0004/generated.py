import re
from urllib.parse import urlparse, urljoin

# External domains considered safe for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedsite.org",
    # Add more domains as needed
]

# Regular expression to detect potentially dangerous URLs (e.g., javascript:)
UNSAFE_SCHEMES = re.compile(r"^(javascript|data):", re.IGNORECASE)


def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    app_home_url : str
        The base URL of the application (e.g., "https://app.example.com").
    forward_param : str
        The user-provided redirect target. May be a relative path or an absolute URL.

    Returns
    -------
    str
        The fully qualified redirect URL that is guaranteed to be either within the base domain
        or an allowed external domain.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or an allowed external domain,
        or if it contains an unsafe scheme.
    """
    # Parse the base application URL
    base_parsed = urlparse(app_home_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("Invalid app_home_url: must contain scheme and netloc")

    # Normalize forward_param
    forward_parsed = urlparse(forward_param)

    # Check for unsafe schemes (e.g., javascript:)
    if UNSAFE_SCHEMES.match(forward_param):
        raise ValueError("Unsafe scheme detected in forward_param")

    # If the forward param is an absolute URL
    if forward_parsed.scheme and forward_parsed.netloc:
        # Ensure the scheme is http or https
        if forward_parsed.scheme not in ("http", "https"):
            raise ValueError("Only http and https schemes are allowed for external redirects")

        # Verify the domain is in ALLOWED_DOMAINS
        if forward_parsed.hostname not in ALLOWED_DOMAINS:
            raise ValueError(f"Domain '{forward_parsed.hostname}' not in ALLOWED_DOMAINS")

        # Return the absolute URL as is (but ensure it uses the same scheme as provided)
        return forward_param

    # If relative path or fragment, join with base
    redirect_url = urljoin(app_home_url.rstrip('/') + '/', forward_param.lstrip('/'))

    # Ensure the resulting URL is still within the base domain
    final_parsed = urlparse(redirect_url)
    if final_parsed.hostname != base_parsed.hostname:
        raise ValueError("Redirect URL resolves to a different domain than the application")

    return redirect_url