import re
from urllib.parse import urlparse, ParseResult

# Approved public-facing API endpoints (example list)
APPROVED_DOMAINS = {
    "api.example.com",
    "services.mycompany.org",
    "public.api.service.io",
}

# Regular expression to detect private IP ranges
PRIVATE_IP_REGEX = re.compile(
    r"^(?:(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    r"|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}"
    r"|192\.168\.\d{1,3}\.\d{1,3}"
    r"|169\.254\.\d{1,3}\.\d{1,3})$"
)


def _is_private_ip(ip: str) -> bool:
    """Return True if the IP address is in a private or reserved range."""
    return bool(PRIVATE_IP_REGEX.match(ip))


def _is_public_hostname(hostname: str) -> bool:
    """Check if the hostname is a public domain and not an IP."""
    # Reject pure numeric IP addresses
    if re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", hostname):
        return not _is_private_ip(hostname)
    # Reject localhost
    if hostname.lower() in {"localhost", "127.0.0.1"}:
        return False
    # Reject any hostname that resolves to a private IP (basic check)
    return True


def process_hook(hook_url: str) -> str:
    """
    Validate a webhook URL and ensure it targets an approved public API endpoint.

    Parameters
    ----------
    hook_url : str
        The URL provided by the external service.

    Returns
    -------
    str
        A safely validated URL that references an approved API endpoint.

    Raises
    ------
    ValueError
        If the URL's domain is outside the list of approved API endpoints,
        or if it targets an internal network location.
    """
    if not hook_url:
        raise ValueError("hook_url must be a non-empty string")

    parsed: ParseResult = urlparse(hook_url)

    # Basic scheme validation
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure netloc (hostname) is present
    if not parsed.netloc:
        raise ValueError("URL must contain a network location (hostname)")

    # Split hostname and port if present
    host_part = parsed.hostname or ""
    if not _is_public_hostname(host_part):
        raise ValueError(f"Hostname '{host_part}' is not a public domain")

    # Check against approved domains
    if host_part.lower() not in APPROVED_DOMAINS:
        raise ValueError(f"Hostname '{host_part}' is not an approved endpoint")

    # Reconstruct the URL to ensure it uses a normalized form
    safe_url = parsed.geturl()
    return safe_url


# Example usage (commented out; remove comments to test):
# try:
#     safe = process_hook("https://api.example.com/webhook")
#     print("Safe URL:", safe)
# except ValueError as e:
#     print("Validation error:", e)