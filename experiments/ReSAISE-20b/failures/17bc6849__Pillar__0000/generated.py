import re
from urllib.parse import urlparse, urljoin

# List of external domains considered safe for redirection
ALLOWED_DOMAINS = [
    "example.com",
    "trusted.org",
    # Add more domains as needed
]

def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    app_home_url : str
        Base URL of the application (e.g., "https://myapp.com/").
    forward_param : str
        Desired redirect path or absolute URL supplied by the user.

    Returns
    -------
    str
        The fully-qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or an allowed external domain.
    """
    # Ensure both inputs are strings
    if not isinstance(app_home_url, str) or not isinstance(forward_param, str):
        raise TypeError("Both app_home_url and forward_param must be strings")

    # Resolve the forward link relative to the application home
    full_url = urljoin(app_home_url, forward_param)

    # Parse the resulting URL
    parsed = urlparse(full_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("Resulting URL is malformed")

    # Determine if the target is internal or external
    app_parsed = urlparse(app_home_url)
    base_netloc = app_parsed.netloc.lower()

    target_netloc = parsed.netloc.lower()

    # Helper to strip leading www for comparison
    def canonical(host: str) -> str:
        return re.sub(r"^www\.", "", host)

    if canonical(target_netloc) == canonical(base_netloc):
        # Internal redirect – allowed
        return full_url

    # External domain: must be in ALLOWED_DOMAINS
    if canonical(target_netloc) not in (canonical(d) for d in ALLOWED_DOMAINS):
        raise ValueError(f"Redirect to external domain '{target_netloc}' is not allowed")

    # External but allowed
    return full_url