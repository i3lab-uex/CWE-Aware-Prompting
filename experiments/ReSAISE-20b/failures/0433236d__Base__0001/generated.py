import re
from urllib.parse import urlparse, urlunparse
import ipaddress

# Whitelist of approved public API domains.
ALLOWED_DOMAINS = {
    "api.example.com",
    "services.partner.org",
    "public-api.mycompany.net",
}

# Regular expression to detect IP addresses in the hostname part.
IP_REGEX = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")


def _is_private_ip(hostname: str) -> bool:
    """
    Determine if a hostname is an IP address that belongs to a private or
    reserved network range.
    """
    try:
        ip = ipaddress.ip_address(hostname)
        return ip.is_private or ip.is_loopback or ip.is_reserved
    except ValueError:
        # Not an IP address; treat as non-private.
        return False


def _validate_hostname(hostname: str) -> None:
    """
    Validate that the hostname is in the allowed list and not a private IP.
    Raises ValueError if validation fails.
    """
    # Check for IP addresses explicitly
    if IP_REGEX.match(hostname):
        if _is_private_ip(hostname):
            raise ValueError(f"Disallowed private IP address: {hostname}")
        # If the IP is public, it must be in ALLOWED_DOMAINS (unlikely)
        if hostname not in ALLOWED_DOMAINS:
            raise ValueError(f"IP address {hostname} is not whitelisted")
        return

    # For domain names, ensure they end with an allowed domain.
    if not any(hostname == domain or hostname.endswith("." + domain)
               for domain in ALLOWED_DOMAINS):
        raise ValueError(f"Domain {hostname} is not whitelisted")


def handle_webhook_request(external_url: str) -> str:
    """
    Validate an external URL supplied by a webhook and return a sanitized
    URL suitable for internal API usage.

    Parameters
    ----------
    external_url : str
        The raw URL received from the webhook payload.

    Returns
    -------
    str
        A validated, normalized URL that can safely be used for internal API calls.

    Raises
    ------
    ValueError
        If the URL contains a disallowed domain or points to a private/internal network.
    """
    if not isinstance(external_url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urlparse(external_url)

    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must have a scheme and netloc")

    # Only allow HTTPS (or optionally HTTP if needed)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Extract hostname (without port)
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL does not contain a valid hostname")

    # Validate the hostname against whitelist and private IPs
    _validate_hostname(hostname)

    # Reconstruct a clean URL (strip fragments, normalize path)
    cleaned = urlunparse((
        parsed.scheme,
        f"{hostname}{':' + str(parsed.port) if parsed.port else ''}",
        parsed.path or "/",
        "",  # params
        parsed.query,
        ""   # fragment
    ))

    return cleaned


# Example usage (for demonstration only; remove or guard in production)
if __name__ == "__main__":
    test_urls = [
        "https://api.example.com/v1/data?x=1",
        "http://services.partner.org/api",
        "https://10.0.0.1/secret",          # private IP
        "https://malicious.com/phish",
    ]

    for url in test_urls:
        try:
            print(f"Validated: {handle_webhook_request(url)}")
        except ValueError as e:
            print(f"Rejected: {url} -> {e}")