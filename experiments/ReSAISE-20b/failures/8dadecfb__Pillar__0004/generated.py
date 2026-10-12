import re
from urllib.parse import urlparse, urlunparse

# Approved domains (can be extended as needed)
APPROVED_DOMAINS = {
    "example.com",
    "trusted.org",
    "safe-site.net",
}

# Regex to detect IP addresses (both IPv4 and IPv6)
IPV4_RE = re.compile(r"""
    ^
    (?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}
    (?:25[0-5]|2[0-4]\d|1?\d{1,2})
    $
""", re.VERBOSE)

IPV6_RE = re.compile(r"""
    ^
    \[
        (?:
            [0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){7}
            |
            ([0-9a-fA-F]{1,4}:){1,7}:
            |
            ([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}
            |
            ([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}
            |
            ([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}
            |
            ([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}
            |
            ([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}
            |
            [0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})
            |
            :((:[0-9a-fA-F]{1,4}){1,7}|:)
        )
    \]
    $
""", re.VERBOSE)

def _is_ip_address(hostname: str) -> bool:
    """Return True if the hostname is an IP address."""
    return IPV4_RE.match(hostname) or IPV6_RE.match(hostname)

def _normalize_hostname(hostname: str) -> str:
    """Return the hostname lower‑cased and stripped of surrounding brackets."""
    return hostname.lower().strip("[]")

def validate_redirect_url(input_url: str) -> str:
    """
    Validate a user‑supplied URL and ensure it redirects only to approved domains.

    Parameters
    ----------
    input_url : str
        The URL provided by the user.

    Returns
    -------
    str
        The original URL if it is safe for redirection.

    Raises
    ------
    ValueError
        If the URL's domain is not in the approved list, or if the URL has an unsafe scheme
        (e.g., file://) or contains an IP address.
    """
    if not input_url:
        raise ValueError("URL must not be empty")

    parsed = urlparse(input_url)

    # Only allow http and https schemes
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    # Extract hostname; urlparse returns '' for netloc without host
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL must contain a valid host")

    # Reject IP addresses
    if _is_ip_address(hostname):
        raise ValueError("Redirect to an IP address is disallowed")

    hostname = _normalize_hostname(hostname)

    # Domain must match one of the approved domains or be a subdomain of them
    if not any(
        hostname == domain or hostname.endswith("." + domain)
        for domain in APPROVED_DOMAINS
    ):
        raise ValueError(f"Domain '{hostname}' is not approved for redirection")

    # Re‑build the URL to ensure it remains unchanged and safe
    safe_url = urlunparse(parsed)
    return safe_url

# Example usage:
if __name__ == "__main__":
    try:
        url = validate_redirect_url("https://sub.example.com/path?query=1")
        print(f"Safe URL: {url}")
    except ValueError as e:
        print(f"Invalid redirect: {e}")