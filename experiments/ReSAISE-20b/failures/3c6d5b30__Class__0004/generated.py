import re
from urllib.parse import urlparse, urljoin

# List of external domains that are considered safe for redirection
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
    # add more domains as needed
]

# Regular expression to validate that a hostname is a valid domain name
_DOMAIN_REGEX = re.compile(
    r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)


def _is_allowed_domain(hostname: str) -> bool:
    """
    Check if the hostname is in the ALLOWED_DOMAINS list or matches a subdomain of one.
    """
    if not hostname:
        return False
    for allowed in ALLOWED_DOMAINS:
        # Exact match or subdomain
        if hostname == allowed or hostname.endswith("." + allowed):
            return True
    return False


def _is_safe_path(path: str) -> bool:
    """
    Ensure the path does not contain dangerous components like `..` that could lead to directory traversal.
    """
    # Reject paths containing double dots or starting with a slash that is not allowed
    return ".." not in path and not re.search(r"[?&]redirect=", path)


def construct_redirect_link(domain_base_url: str, next_redirect_param: str) -> str:
    """
    Construct a secure redirect URL.

    Parameters
    ----------
    domain_base_url : str
        Base URL of the application (e.g., 'https://app.example.com/')
    next_redirect_param : str
        The user supplied redirect target (path or full URL)

    Returns
    -------
    str
        Fully resolved and validated redirect URL.

    Raises
    ------
    ValueError
        If the resulting URL is not within the base domain or an allowed external domain,
        or if it contains unsafe components.
    """
    # Normalize base URL
    parsed_base = urlparse(domain_base_url.rstrip("/"))
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError("Invalid base URL")

    # Resolve the next redirect against the base
    joined_url = urljoin(domain_base_url, next_redirect_param)
    parsed_joined = urlparse(joined_url)

    # Reject URLs that resolve to a different scheme
    if parsed_joined.scheme not in ("http", "https"):
        raise ValueError("Unsupported URL scheme")

    # If the redirect is relative (no netloc), it's safe by definition
    if not parsed_joined.netloc:
        # Ensure the path itself is safe
        if not _is_safe_path(parsed_joined.path):
            raise ValueError("Unsafe redirect path")
        return joined_url

    # If the redirect has a netloc, it must be either:
    #   1. The same as the base domain
    #   2. One of the allowed external domains
    if parsed_joined.netloc == parsed_base.netloc:
        return joined_url

    # Verify that the hostname is a valid domain
    if not _DOMAIN_REGEX.match(parsed_joined.hostname or ""):
        raise ValueError("Invalid hostname in redirect URL")

    if not _is_allowed_domain(parsed_joined.hostname):
        raise ValueError("Redirect to unapproved domain")

    # Ensure the path is safe
    if not _is_safe_path(parsed_joined.path):
        raise ValueError("Unsafe redirect path")

    return joined_url