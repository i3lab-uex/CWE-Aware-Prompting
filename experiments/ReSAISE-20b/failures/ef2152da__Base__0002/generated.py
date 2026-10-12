import socket
import ipaddress
from urllib.parse import urlparse, urlunparse

# ------------------------------------------------------------------
# Whitelisted public API endpoints (scheme + hostname). Adjust as needed.
WHITELISTED_ENDPOINTS = {
    ("https", "api.example.com"),
    ("https", "public-api.service.org"),
    ("http",  "data.provider.net"),
}

# ------------------------------------------------------------------
def _is_private_ip(ip: str) -> bool:
    """
    Check whether an IP address is in a private or reserved range.
    """
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        # Not a valid IP address (e.g., domain name)
        return False


def _resolve_host(hostname: str) -> list[str]:
    """
    Resolve a hostname to its IP addresses.
    Returns a list of stringified IPs.
    """
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return []

    ips = []
    for info in infos:
        ip = info[4][0]
        if ip not in ips:
            ips.append(ip)
    return ips


def validate_callback(callback_url: str) -> str:
    """
    Validate a webhook URL before it is used for internal API calls.

    Parameters
    ----------
    callback_url : str
        The external webhook URL supplied by an upstream component.

    Returns
    -------
    str
        A normalized, validated URL that is safe for internal use.

    Raises
    ------
    ValueError
        If the URL's host is not in the whitelist or resolves to a private IP.
    """
    if not callback_url:
        raise ValueError("callback_url must be a non-empty string")

    parsed = urlparse(callback_url)

    # Basic scheme check
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    # Ensure hostname is present
    if not parsed.hostname:
        raise ValueError("URL must contain a valid hostname")

    # Check against whitelist
    if (parsed.scheme, parsed.hostname) not in WHITELISTED_ENDPOINTS:
        raise ValueError(f"Hostname {parsed.hostname} is not in the whitelist")

    # Resolve hostname to IPs and ensure none are private
    for ip in _resolve_host(parsed.hostname):
        if _is_private_ip(ip):
            raise ValueError(
                f"Hostname {parsed.hostname} resolves to private IP: {ip}"
            )

    # Reconstruct the URL to normalize it (e.g., strip default ports)
    netloc = parsed.hostname
    if parsed.port:
        # Only include port if it is non-default for the scheme
        default_port = {"http": 80, "https": 443}[parsed.scheme]
        if parsed.port != default_port:
            netloc += f":{parsed.port}"

    safe_url = urlunparse(
        (
            parsed.scheme,
            netloc,
            parsed.path or "/",
            "",  # params
            parsed.query,
            parsed.fragment,
        )
    )

    return safe_url


# ------------------------------------------------------------------
if __name__ == "__main__":
    # Example usage
    test_urls = [
        "https://api.example.com/webhook",
        "http://data.provider.net:80/endpoint?token=abc",
        "https://malicious.local/evil",
    ]

    for url in test_urls:
        try:
            print(f"Validating: {url}")
            result = validate_callback(url)
            print(f"  -> Safe URL: {result}\n")
        except ValueError as exc:
            print(f"  -> Validation failed: {exc}\n")