import urllib.parse
from typing import List

# Example list of allowed external domains. In real usage, populate this appropriately.
ALLOWED_DOMAINS: List[str] = [
    "example.com",
    "trustedpartner.org",
    # Add more domains as needed
]

def create_forward_link(app_home_url: str, forward_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    app_home_url : str
        Base URL of the application (e.g., "https://app.example.com/").
    forward_param : str
        User-provided path or absolute URL to redirect to.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or an allowed external domain.
    """
    # Ensure app_home_url ends with a slash for correct joining
    base = urllib.parse.urljoin(app_home_url.rstrip('/') + '/', '')

    # Parse the forward parameter
    parsed_forward = urllib.parse.urlparse(forward_param)

    if parsed_forward.scheme in ("http", "https"):
        # Absolute URL: validate domain
        netloc = parsed_forward.netloc.lower()
        if not any(netloc == d or netloc.endswith("." + d) for d in ALLOWED_DOMAINS):
            raise ValueError(f"Disallowed external domain: {netloc}")
        # Reconstruct the URL to ensure it is fully qualified
        redirect_url = parsed_forward.geturl()
    else:
        # Relative path: join with base
        redirect_url = urllib.parse.urljoin(base, forward_param)

    # Final validation: ensure the URL points to app_home_url or an allowed domain
    final_parsed = urllib.parse.urlparse(redirect_url)
    final_netloc = final_parsed.netloc.lower()

    # Check that the URL is either inside the base domain or an allowed external domain
    if final_netloc:
        # If it has a netloc, it must be in ALLOWED_DOMAINS
        if not any(final_netloc == d or final_netloc.endswith("." + d) for d in ALLOWED_DOMAINS):
            raise ValueError(f"Redirect URL points to disallowed domain: {final_netloc}")
    else:
        # No netloc means a relative path; ensure it doesn't contain dangerous patterns
        if ".." in urllib.parse.unquote(final_parsed.path):
            raise ValueError("Redirect path contains directory traversal components")

    return redirect_url