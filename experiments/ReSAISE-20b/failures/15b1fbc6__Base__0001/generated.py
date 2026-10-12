import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of domains that are considered safe for redirection.
APPROVED_DOMAINS = {
    "example.com",
    "safe.org",
    # Add other approved domains here
}

# Regular expression to detect IP addresses in the hostname.
IP_REGEX = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$|^\[?[A-Fa-f0-9:]+\]?$")


def handle_user_redirect(user_url: str) -> str:
    """
    Validate and sanitize a user-provided URL before redirecting.

    Parameters
    ----------
    user_url : str
        The raw URL supplied by the user.

    Returns
    -------
    str
        A sanitized, fully-qualified URL that can be safely used for redirection.

    Raises
    ------
    ValueError
        If the URL is malformed, uses an unsafe scheme,
        contains a private or reserved IP address,
        or its domain is not in the list of approved domains.
    """
    # Parse the URL and ensure it has a scheme
    parsed = urlparse(user_url)
    if not parsed.scheme or parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL must use http or https scheme")

    # Reject URLs that point to private, loopback, link-local or reserved IPs
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid hostname")

    # If the host looks like an IP address, validate it
    if IP_REGEX.match(hostname):
        try:
            ip = ipaddress.ip_address(hostname)
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                raise ValueError("URL points to a private or reserved IP address")
        except ValueError:
            # hostname is not a valid IP; continue with normal validation
            pass

    # Normalize the domain (lowercase, strip trailing dot)
    normalized_domain = hostname.lower().rstrip(".")

    # Check if the domain is in the approved list or a subdomain of an approved domain
    if not any(
        normalized_domain == ad or normalized_domain.endswith("." + ad)
        for ad in APPROVED_DOMAINS
    ):
        raise ValueError(f"Domain '{normalized_domain}' is not approved for redirection")

    # Reconstruct the URL to ensure it has no user info or port issues
    sanitized = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,  # includes hostname and port if present
            parsed.path or "",
            "",  # params are deprecated in URLs
            parsed.query,
            parsed.fragment,
        )
    )

    return sanitized