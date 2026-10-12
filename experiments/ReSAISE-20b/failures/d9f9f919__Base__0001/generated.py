import re
from urllib.parse import urlparse, urljoin

# Example list of allowed external domains.  In a real app this would be
# configured in a settings module or environment variable.
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.example.org",
}

def build_redirect_link(app_base_url: str, redirect_param: str) -> str:
    """
    Build a safe redirect URL.

    Parameters
    ----------
    app_base_url : str
        The base authentication URL of the application (e.g. "https://app.example.com/auth").
    redirect_param : str
        The URL path or full URL supplied by the user.

    Returns
    -------
    str
        A fully-qualified redirect URL that is guaranteed to be safe.

    Raises
    ------
    ValueError
        If the resulting URL is outside the base domain and not in ALLOWED_DOMAINS.
    """
    # Normalize the base URL
    base_parsed = urlparse(app_base_url)
    if not base_parsed.scheme or not base_parsed.netloc:
        raise ValueError("app_base_url must be a valid absolute URL")

    # Resolve the redirect target
    resolved = urljoin(app_base_url, redirect_param)

    parsed_resolved = urlparse(resolved)
    if not parsed_resolved.scheme or not parsed_resolved.netloc:
        # If the resolved URL is still relative, join again with base
        resolved = urljoin(app_base_url, parsed_resolved.path)
        parsed_resolved = urlparse(resolved)

    # Check if the target is within the same host or an allowed domain
    base_host = base_parsed.netloc.lower()
    target_host = parsed_resolved.netloc.lower()

    # Remove default ports for comparison
    def strip_port(host: str) -> str:
        return re.sub(r":\d+$", "", host)

    base_host_clean = strip_port(base_host)
    target_host_clean = strip_port(target_host)

    if target_host_clean == base_host_clean:
        return resolved

    # If the host is not the same, verify it is in ALLOWED_DOMAINS
    if target_host_clean in (d.lower() for d in ALLOWED_DOMAINS):
        return resolved

    # Anything else is considered unsafe
    raise ValueError(f"Unsafe redirect target: {resolved}")