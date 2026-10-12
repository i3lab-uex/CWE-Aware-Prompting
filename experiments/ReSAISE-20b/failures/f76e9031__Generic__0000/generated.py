import re
from urllib.parse import urlparse, urlunparse

# List of domains that are considered safe for redirection
APPROVED_DOMAINS = {
    "example.com",
    "trustedsite.org",
    "safe-redirect.net",
}

# Allowed URL schemes
ALLOWED_SCHEMES = {"http", "https"}

def redirect_user_safely(target_url: str) -> str:
    """
    Validate that the supplied URL points to an approved domain and has a safe scheme.
    
    Parameters
    ----------
    target_url : str
        The user‑supplied URL to redirect to.
    
    Returns
    -------
    str
        Normalised, validated URL that is safe for redirection.
    
    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list, or if it uses an
        unsupported scheme or contains disallowed components.
    """
    # Parse the URL
    parsed = urlparse(target_url)

    # Reject relative URLs or URLs without a scheme
    if not parsed.scheme:
        raise ValueError("URL must include a scheme (http:// or https://).")

    # Ensure the scheme is allowed
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(f"Unsupported scheme '{parsed.scheme}'. Only HTTP and HTTPS are allowed.")

    # Extract the host (netloc may contain port; we strip it)
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname.")

    # Normalise the host to lowercase for comparison
    host = host.lower()

    # Reject URLs with embedded credentials (user:pass@host)
    if parsed.username or parsed.password:
        raise ValueError("URL must not contain user credentials.")

    # Reject URLs with IP addresses (optional but more secure)
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host):
        raise ValueError("IP addresses are not allowed as redirect targets.")

    # Check if the host ends with an approved domain
    if not any(host == d or host.endswith("." + d) for d in APPROVED_DOMAINS):
        raise ValueError(f"Domain '{host}' is not approved for redirection.")

    # Disallow fragments and query parameters that might alter the target
    if parsed.fragment:
        raise ValueError("URL must not contain a fragment (#...).")

    # Reconstruct the URL with only allowed components
    safe_parsed = parsed._replace(
        username=None,
        password=None,
        fragment="",
    )
    safe_url = urlunparse(safe_parsed)

    return safe_url