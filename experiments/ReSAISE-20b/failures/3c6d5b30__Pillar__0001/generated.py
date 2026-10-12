# ────────────────────────────────────────────────────────────── #
#  Safe redirect link constructor – prevents open‑redirect attacks
# ────────────────────────────────────────────────────────────── #

from urllib.parse import urlparse, urljoin

# Example list of external domains considered safe for redirection.
# In a real application this should be populated with the exact
# domains that are allowed (e.g. ["https://example.com", ...]).
ALLOWED_DOMAINS = [
    "https://trusted-redirect.example.com",
    "https://another-safe-site.org",
]

def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a safe redirect URL after login.

    Parameters
    ----------
    domain_base_url : str
        The base URL of the application (e.g. "https://myapp.com").
    next_redirect_param : str
        The URL path or address the user wants to navigate to after login.
        It may be a relative path (e.g. "/dashboard") or an absolute URL.

    Returns
    -------
    str
        The fully qualified redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or one of the
        allowed external domains. This protects against open‑redirect
        vulnerabilities (CWE‑601) and ensures proper resource control.
    """
    if not domain_base_url:
        raise ValueError("Base URL must be provided")

    # Normalize the base URL (remove trailing slash for consistency)
    base = domain_base_url.rstrip('/')

    # Parse the user-provided redirect
    parsed_next = urlparse(next_redirect_param)

    # If the redirect is relative (no scheme or netloc), join it with base
    if not parsed_next.scheme and not parsed_next.netloc:
        # urljoin will resolve relative paths correctly
        full_url = urljoin(base + '/', next_redirect_param)
    else:
        # Absolute URL: verify that the domain is allowed
        full_url = next_redirect_param

    parsed_full = urlparse(full_url)

    # Ensure the resulting URL has a scheme
    if not parsed_full.scheme:
        raise ValueError("Redirect URL must have a valid scheme (http or https)")

    # Check if the redirect is internal to the base domain
    base_parsed = urlparse(base)
    if parsed_full.netloc == base_parsed.netloc:
        return full_url

    # If not internal, ensure the domain is in ALLOWED_DOMAINS
    allowed = False
    for allowed_url in ALLOWED_DOMAINS:
        parsed_allowed = urlparse(allowed_url)
        if (parsed_full.scheme, parsed_full.netloc) == (parsed_allowed.scheme, parsed_allowed.netloc):
            allowed = True
            break

    if not allowed:
        raise ValueError("Redirect URL is not within the base domain or an allowed external domain")

    return full_url