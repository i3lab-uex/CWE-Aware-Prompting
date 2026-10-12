import re
from urllib.parse import urlparse, urljoin

# Domains that are considered safe for external redirects.
APPROVED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # add more domains as needed
]

def _is_safe_domain(url: str) -> bool:
    """
    Check if the given URL belongs to the application domain or an approved external domain.
    """
    parsed = urlparse(url)
    # If the URL has no netloc, it's a relative path – considered safe.
    if not parsed.netloc:
        return True

    # Allow only http/https schemes for external URLs.
    if parsed.scheme not in ("http", "https"):
        return False

    # Strip port for comparison
    hostname = parsed.hostname or ""
    if ":" in hostname:
        hostname = hostname.split(":")[0]

    # Check against approved domains
    return any(hostname.lower() == domain.lower() for domain in APPROVED_DOMAINS)


def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Generate a secure redirect URL based on the user's 'next' parameter.

    Parameters
    ----------
    app_url : str
        Base URL of the application (e.g., "https://myapp.com/").
    redirect_param : str
        User-provided path or URL to redirect to after login.

    Returns
    -------
    str
        The full, validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the application domain or an approved external domain.
    """
    # Ensure base app_url ends with a slash for urljoin to work correctly
    if not app_url.endswith("/"):
        base = f"{app_url}/"
    else:
        base = app_url

    # Sanitize the redirect_param to avoid directory traversal or protocol injection
    if not isinstance(redirect_param, str):
        raise ValueError("Redirect parameter must be a string")

    # Reject dangerous patterns like '//' at the start which could escape base URL
    if re.match(r"^//", redirect_param):
        raise ValueError("Invalid redirect parameter: leading '//' not allowed")

    # Build the full URL
    candidate = urljoin(base, redirect_param)

    # Validate that the resulting URL stays within allowed domains
    parsed_candidate = urlparse(candidate)
    if not _is_safe_domain(candidate):
        raise ValueError(f"Unsafe redirect URL: {candidate}")

    # Ensure the path is absolute (starts with '/')
    if not parsed_candidate.path.startswith("/"):
        raise ValueError("Redirect path must be absolute")

    return candidate