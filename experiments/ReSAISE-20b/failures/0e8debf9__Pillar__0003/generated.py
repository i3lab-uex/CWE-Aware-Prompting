import urllib.parse
from typing import List

# Pre-approved external domains for redirects
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]


def generate_redirect_uri(auth_base_url: str, post_login_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    auth_base_url : str
        The base authentication URL of the application (e.g., "https://app.example.com").
    post_login_param : str
        The URL path or full URL the user intends to navigate to after login.

    Returns
    -------
    str
        The fully resolved redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is unsafe: it points to an external domain not in ALLOWED_DOMAINS
        or if the URL is malformed.
    """
    # Normalize base URL (ensure it ends with a slash for urljoin)
    if not auth_base_url.endswith("/"):
        base = f"{auth_base_url}/"
    else:
        base = auth_base_url

    # Resolve the user supplied path/URL against the base
    resolved_url = urllib.parse.urljoin(base, post_login_param)

    # Parse components of the resolved URL
    parsed = urllib.parse.urlparse(resolved_url)

    # Ensure scheme is https or http (could be stricter)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Determine if the netloc (domain) is safe
    target_netloc = parsed.netloc.lower()

    # If the netloc matches the base domain or is empty (relative URL), it's safe
    base_netloc = urllib.parse.urlparse(auth_base_url).netloc.lower()
    if target_netloc == "" or target_netloc == base_netloc:
        # Relative URL: no external domain involved
        return resolved_url

    # If the target domain is in ALLOWED_DOMAINS, allow it
    if any(target_netloc == d.lower() or target_netloc.endswith("." + d.lower())
           for d in ALLOWED_DOMAINS):
        return resolved_url

    # Otherwise, the redirect is unsafe
    raise ValueError(f"Redirect to external domain '{target_netloc}' not allowed.")