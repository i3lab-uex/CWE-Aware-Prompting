import re
from urllib.parse import urlparse, urljoin

# Domains that are explicitly allowed for redirection.
ALLOWED_DOMAINS = [
    "example.com",
    "trustedpartner.org",
]

def _is_safe_domain(domain: str) -> bool:
    """
    Check whether a domain is the same as the base domain or in ALLOWED_DOMAINS.
    """
    # Remove leading 'www.' for comparison
    domain = domain.lower().lstrip("www.")
    return any(domain == d or domain.endswith(f".{d}") for d in ALLOWED_DOMAINS)


def create_redirect_url(base_url: str, next_param: str) -> str:
    """
    Build a safe redirect URL.

    Parameters
    ----------
    base_url : str
        The application's base URL (e.g. "https://app.example.com/").
    next_param : str
        User supplied redirect target.

    Returns
    -------
    str
        The fully resolved, safe URL to redirect the user to.

    Raises
    ------
    ValueError
        If the resulting URL is not within the same domain as `base_url`
        or is not in the list of allowed external domains.
    """
    if not base_url:
        raise ValueError("Base URL must be provided")

    # Parse the base URL to get its components
    parsed_base = urlparse(base_url)
    if not parsed_base.scheme or not parsed_base.netloc:
        raise ValueError(f"Invalid base URL: {base_url}")

    # If next_param is empty, just return the base URL
    if not next_param:
        return base_url

    # Resolve the next parameter against the base URL
    resolved = urljoin(base_url, next_param)

    # Parse the resulting URL to inspect its domain
    parsed_resolved = urlparse(resolved)

    # Ensure the resolved URL uses a safe scheme
    if parsed_resolved.scheme not in {"http", "https"}:
        raise ValueError(f"Unsafe scheme: {parsed_resolved.scheme}")

    # If the resolved URL is relative (no netloc), it is safe
    if not parsed_resolved.netloc:
        return resolved

    # Compare domains: must match base domain or be allowed
    base_domain = parsed_base.netloc.lower()
    target_domain = parsed_resolved.netloc.lower()

    # Normalize by stripping 'www.'
    base_clean = base_domain.lstrip("www.")
    target_clean = target_domain.lstrip("www.")

    if target_clean == base_clean:
        return resolved

    # If not the same domain, check against allowed domains
    if _is_safe_domain(target_clean):
        return resolved

    raise ValueError(f"Redirect URL domain not allowed: {target_domain}")