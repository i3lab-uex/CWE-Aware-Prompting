import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# List of domains that are allowed for redirection.
ALLOWED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net",
}

# Regular expression to detect IP addresses in the host part
IP_PATTERN = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")


def _is_ip_address(host: str) -> bool:
    """
    Check if the provided host string is an IP address.
    """
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _is_allowed_domain(host: str) -> bool:
    """
    Verify that the host is either a sub‑domain of an allowed domain or
    exactly matches one of the approved domains.
    """
    # Reject pure IP addresses
    if _is_ip_address(host):
        return False

    # Normalize host (lowercase, strip trailing dot)
    host = host.lower().rstrip(".")

    # Direct match
    if host in ALLOWED_DOMAINS:
        return True

    # Sub‑domain match (e.g., sub.example.com)
    for allowed in ALLOWED_DOMAINS:
        if host.endswith("." + allowed):
            return True

    return False


def secure_user_redirect(url_input: str) -> str:
    """
    Validate a user‑supplied URL against a whitelist of safe domains.

    Parameters
    ----------
    url_input : str
        The URL provided by the user.

    Returns
    -------
    str
        A fully validated, safe-to‑use URL suitable for redirection.

    Raises
    ------
    ValueError
        If the supplied URL is malformed, uses an unsafe scheme,
        or its domain is not in the whitelist.
    """
    if not isinstance(url_input, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(url_input)

    # Ensure scheme is http or https
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (host + optional port) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a host component")

    # Separate hostname and port
    host = parsed.hostname
    if not host:
        raise ValueError("URL must contain a valid hostname")

    # Validate the domain
    if not _is_allowed_domain(host):
        raise ValueError(f"Domain '{host}' is not approved for redirection")

    # Reconstruct the URL to ensure it is clean
    safe_url = urlunparse((
        parsed.scheme,
        parsed.netloc,  # preserves port if present
        parsed.path or "/",
        "",             # params are deprecated in URLs; strip them
        parsed.query,
        ""              # no fragment for redirects
    ))

    return safe_url


# Example usage (uncomment to test)
# try:
#     print(secure_user_redirect("https://sub.example.com/path?query=1"))
# except ValueError as e:
#     print(f"Redirect blocked: {e}")