import re
from urllib.parse import urlparse, urljoin

# List of external domains that are explicitly allowed for redirects
APPROVED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def _is_safe_domain(parsed_url: urlparse) -> bool:
    """
    Determine if the parsed URL points to an approved domain or is a relative path.
    """
    # Empty netloc indicates a relative URL (e.g., "/dashboard")
    if not parsed_url.netloc:
        return True

    # Normalize the domain to lower case for comparison
    domain = parsed_url.netloc.lower()

    # Remove port if present
    if ":" in domain:
        domain = domain.split(":")[0]

    # Check against approved domains
    return domain in APPROVED_DOMAINS


def generate_redirect_link(app_url: str, redirect_param: str) -> str:
    """
    Generate a safe redirect URL.

    Parameters
    ----------
    app_url : str
        The base URL of the application (e.g., "https://myapp.com/").
    redirect_param : str
        The URL path or full URL supplied by the user.

    Returns
    -------
    str
        A fully qualified redirect URL that is guaranteed to point within the
        application domain or an approved external domain.

    Raises
    ------
    ValueError
        If the resolved URL points to a disallowed domain or cannot be parsed.
    """
    if not app_url:
        raise ValueError("app_url must be provided")

    # Ensure app_url ends with a slash for proper urljoin handling
    base = app_url if app_url.endswith("/") else f"{app_url}/"

    # Resolve the redirect parameter relative to the base URL
    resolved = urljoin(base, redirect_param)

    parsed_resolved = urlparse(resolved)

    # Validate that the resolved URL is within an approved domain
    if not _is_safe_domain(parsed_resolved):
        raise ValueError(f"Disallowed redirect target: {resolved}")

    # Reconstruct the URL to ensure a consistent format
    safe_url = parsed_resolved.geturl()
    return safe_url


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     print(generate_redirect_link("https://myapp.com", "/profile"))
#     print(generate_redirect_link("https://myapp.com", "https://example.com/welcome"))
#     # The following would raise ValueError:
#     # print(generate_redirect_link("https://myapp.com", "http://malicious.com"))