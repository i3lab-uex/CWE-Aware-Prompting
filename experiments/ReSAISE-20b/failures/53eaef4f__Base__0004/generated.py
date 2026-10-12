from urllib.parse import urlparse, urljoin, urlunparse

# Domains that are explicitly allowed for redirects (e.g. trusted partners)
SAFE_DOMAINS = [
    "trusted.example.com",
    "partner.org",
]

def build_redirect_uri(primary_url: str, next_path: str) -> str:
    """
    Construct a safe redirect URL based on the user supplied `next_path`.

    Parameters
    ----------
    primary_url : str
        The base URL of the application (e.g. "https://app.example.com").
    next_path : str
        The URL path or full URL supplied by the user.

    Returns
    -------
    str
        A fully qualified redirect URL that is guaranteed to be either
        relative to the application or point to a domain in SAFE_DOMAINS.

    Raises
    ------
    ValueError
        If the constructed URL would redirect to a domain outside the
        application or `SAFE_DOMAINS`.
    """
    # Parse the primary URL once
    base_parsed = urlparse(primary_url)

    # If next_path is an absolute URL, we need to validate its domain
    parsed_next = urlparse(next_path)

    if parsed_next.scheme and parsed_next.netloc:
        # It's an absolute URL. Validate the host.
        target_host = parsed_next.hostname.lower() if parsed_next.hostname else ""

        # Allow if the host matches the primary app's host
        if target_host == base_parsed.hostname.lower():
            # Reconstruct the URL to ensure consistent scheme/port
            return urlunparse(parsed_next)

        # Or allow if host is in the list of trusted domains
        if target_host in SAFE_DOMAINS:
            return urlunparse(parsed_next)

        # Otherwise reject
        raise ValueError(f"Redirect to untrusted domain: {target_host}")

    # If it's a relative path, safely join it with the base URL
    # This also normalizes paths like "../etc/passwd" to stay within the domain.
    joined = urljoin(primary_url, next_path)

    # Ensure that the resulting URL hasn't escaped the base domain
    joined_parsed = urlparse(joined)
    if joined_parsed.hostname.lower() != base_parsed.hostname.lower():
        raise ValueError(f"Redirect escaped application domain: {joined}")

    return joined