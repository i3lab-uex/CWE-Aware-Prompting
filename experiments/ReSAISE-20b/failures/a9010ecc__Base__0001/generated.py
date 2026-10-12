import re
from urllib.parse import urlparse, urljoin

# List of external domains that are safe for redirection
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # add more domains as needed
]

def generate_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Construct a safe redirect URL.

    Parameters
    ----------
    app_base_url : str
        Base URL of the application (e.g., "https://app.example.com").
    redirect_param : str
        User-provided path or absolute URL to redirect to.

    Returns
    -------
    str
        A fully-qualified, safe redirect URL.

    Raises
    ------
    ValueError
        If the target is not within the base domain or not in ALLOWED_DOMAINS.
    """
    if not app_base_url:
        raise ValueError("app_base_url must be provided")

    # Normalize the base URL
    base_parsed = urlparse(app_base_url.rstrip('/'))
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("app_base_url must be a valid absolute URL")

    # Ensure redirect_param is not empty
    if not redirect_param:
        raise ValueError("redirect_param must be provided")

    # Strip any leading/trailing whitespace
    redirect_param = redirect_param.strip()

    # Check if the redirect is an absolute URL
    target_parsed = urlparse(redirect_param)

    # If the redirect is absolute (has scheme and netloc)
    if target_parsed.scheme in ("http", "https") and target_parsed.netloc:
        # Allow only if the domain is in ALLOWED_DOMAINS
        target_domain = target_parsed.netloc.lower()
        # Remove port if present for comparison
        target_domain = re.sub(r":\d+$", "", target_domain)

        if target_domain not in [d.lower() for d in ALLOWED_DOMAINS]:
            raise ValueError(f"Redirection to external domain '{target_domain}' is not allowed")

        # Return the absolute URL as is (already safe)
        return redirect_param

    # If the redirect is relative or path-only
    # Reject any leading scheme (e.g., "//evil.com") which could be interpreted as absolute
    if redirect_param.startswith("//"):
        raise ValueError("Relative redirects cannot start with '//'")

    # Ensure the path starts with a single slash
    if not redirect_param.startswith("/"):
        redirect_param = "/" + redirect_param

    # Build the final URL by joining with base
    full_url = urljoin(app_base_url, redirect_param)

    # Parse again to ensure the resulting URL is within the base domain
    final_parsed = urlparse(full_url)
    if final_parsed.netloc.lower() != base_parsed.netloc.lower():
        raise ValueError("Redirect leads outside the base domain")

    return full_url